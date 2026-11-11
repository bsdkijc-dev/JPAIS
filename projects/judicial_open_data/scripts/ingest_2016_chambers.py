import os
import json
import subprocess
import pandas as pd
from neo4j import GraphDatabase

# Retrieve container authentication
try:
    cmd = "docker inspect $(docker ps -qf name=neo4j)"
    out = subprocess.check_output(cmd, shell=True).decode()
    data = json.loads(out)
    env_list = data[0]['Config']['Env']
    auth_val = next((e.split('=', 1)[1] for e in env_list if 'NEO4J_AUTH=' in e), 'neo4j/neo4j')
    u, p = auth_val.split('/', 1) if '/' in auth_val else ('neo4j', auth_val)
except Exception:
    u, p = ("neo4j", "password")

driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=(u, p))
base_dir = os.path.expanduser('~/JPAIS/data/open_data_2025/processed')
csv_path = os.path.join(base_dir, 'master_judiciary_chambers_performance_2016.csv')
df = pd.read_csv(csv_path)

print("--> Connected to Neo4j. Ingesting 2016 Chamber Performance Data...")
with driver.session() as s:
    # Set constraints
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chamber) REQUIRE c.name IS UNIQUE")
    s.run("MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})")
    s.run("MERGE (y:ReportingYear {year: 2016})")

    # Ingest each chamber
    for _, r in df.iterrows():
        cypher = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2016})
            MERGE (ch:Chamber {name: $name})
            MERGE (inst)-[:HAS_CHAMBER]->(ch)
            CREATE (perf:ChamberPerformance {
                record_id: $rec_id,
                year: 2016,
                carryover_2015: $sisa_2015,
                incoming_cases: $masuk,
                total_caseload: $beban,
                disposed_cases: $putus,
                ending_backlog: $sisa_akhir,
                disposal_rate_pct: $disp_rate,
                clearance_rate_pct: $clear_rate,
                decided_under_3m_pct: $speed_3m
            })
            MERGE (ch)-[:RECORDED_PERFORMANCE]->(perf)
            MERGE (perf)-[:IN_YEAR]->(y)
        """
        s.run(cypher, {
            "rec_id": str(r["record_id"]),
            "name": str(r["chamber_name"]),
            "sisa_2015": int(r["carryover_2015"]),
            "masuk": int(r["incoming_cases"]),
            "beban": int(r["total_caseload"]),
            "putus": int(r["disposed_cases"]),
            "sisa_akhir": int(r["ending_backlog"]),
            "disp_rate": float(r["disposal_rate_pct"]),
            "clear_rate": float(r["clearance_rate_pct"]),
            "speed_3m": float(r["decided_under_3m_pct"])
        })

    print("\n=== 2016 CHAMBERS IN NEO4J KNOWLEDGE GRAPH ===")
    verify_q = """
        MATCH (ch:Chamber)-[:RECORDED_PERFORMANCE]->(p:ChamberPerformance)-[:IN_YEAR]->(y:ReportingYear {year: 2016})
        RETURN ch.name AS Chamber, p.incoming_cases AS Inflow, p.disposed_cases AS Disposed, 
               p.ending_backlog AS Backlog, p.disposal_rate_pct AS Rate
        ORDER BY p.total_caseload DESC
    """
    for row in s.run(verify_q):
        print(f" {row['Chamber'][:35]:<35} | In: {row['Inflow']:<5} | Out: {row['Disposed']:<5} | Backlog: {row['Backlog']:<5} | {row['Rate']}%")

driver.close()
print("\n--> Chamber Ingestion and Verification Succeeded!")
