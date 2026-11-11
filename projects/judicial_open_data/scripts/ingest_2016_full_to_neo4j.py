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

f_chambers = os.path.join(base_dir, 'master_judiciary_chambers_performance_2016.csv')
f_jurisdictions = os.path.join(base_dir, 'master_judiciary_jurisdictions_caseload_2016.csv')
f_policy = os.path.join(base_dir, 'master_judiciary_strategic_indicators_2016.csv')

df_chambers = pd.read_csv(f_chambers)
df_jurisdictions = pd.read_csv(f_jurisdictions)
df_policy = pd.read_csv(f_policy)

print("--> Connecting to Neo4j. Ingesting Full 2016 Dataset Corpus...")

with driver.session() as s:
    # 1. Setup Constraints
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chamber) REQUIRE c.name IS UNIQUE")
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (j:Jurisdiction) REQUIRE j.name IS UNIQUE")
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:StrategicPolicy) REQUIRE p.record_id IS UNIQUE")
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (y:ReportingYear) REQUIRE y.year IS UNIQUE")
    
    # 2. Merge Root Nodes
    s.run("""
        MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})
        MERGE (y:ReportingYear {year: 2016})
        MERGE (src:SourceDocument {name: 'Laporan Tahunan 2016 Mahkamah Agung RI', publication_year: 2017, isbn: '978-979-8512-94-0'})
        MERGE (inst)-[:PUBLISHED]->(src)
        MERGE (src)-[:COVERS_YEAR]->(y)
    """)

    # 3. Ingest Chambers Performance (7 Chambers)
    for _, r in df_chambers.iterrows():
        cypher_ch = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2016})
            MERGE (ch:Chamber {name: $name})
            MERGE (inst)-[:HAS_CHAMBER]->(ch)
            MERGE (perf:ChamberPerformance {record_id: $rec_id})
            SET perf.year = 2016,
                perf.carryover_2015 = $sisa_2015,
                perf.incoming_cases = $masuk,
                perf.total_caseload = $beban,
                perf.disposed_cases = $putus,
                perf.ending_backlog = $sisa_akhir,
                perf.disposal_rate_pct = $disp_rate,
                perf.clearance_rate_pct = $clear_rate,
                perf.decided_under_3m_pct = $speed_3m
            MERGE (ch)-[:RECORDED_PERFORMANCE]->(perf)
            MERGE (perf)-[:IN_YEAR]->(y)
        """
        s.run(cypher_ch, {
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
    print(f" - Ingested {len(df_chambers)} Chamber Performance records.")

    # 4. Ingest Jurisdiction Caseload (5 Jurisdictions)
    for _, r in df_jurisdictions.iterrows():
        cypher_jur = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2016})
            MERGE (jur:Jurisdiction {name: $name})
            MERGE (inst)-[:HAS_JURISDICTION]->(jur)
            MERGE (caseload:JurisdictionCaseload {record_id: $rec_id})
            SET caseload.year = 2016,
                caseload.carryover_2015 = $sisa_2015,
                caseload.incoming_cases = $masuk,
                caseload.total_caseload = $beban,
                caseload.disposed_cases = $putus,
                caseload.withdrawn_cases = $cabut,
                caseload.ending_backlog = $sisa_akhir,
                caseload.disposal_rate_pct = $disp_rate,
                caseload.backlog_ratio_pct = $backlog_rate
            MERGE (jur)-[:RECORDED_CASELOAD]->(caseload)
            MERGE (caseload)-[:IN_YEAR]->(y)
        """
        s.run(cypher_jur, {
            "rec_id": str(r["record_id"]),
            "name": str(r["jurisdiction"]),
            "sisa_2015": int(r["carryover_2015"]),
            "masuk": int(r["incoming_cases"]),
            "beban": int(r["total_caseload"]),
            "putus": int(r["disposed_cases"]),
            "cabut": int(r["withdrawn_cases"]),
            "sisa_akhir": int(r["ending_backlog"]),
            "disp_rate": float(r["disposal_rate_pct"]),
            "backlog_rate": float(r["backlog_ratio_pct"])
        })
    print(f" - Ingested {len(df_jurisdictions)} Jurisdiction Caseload records.")

    # 5. Ingest Strategic Policy Indicators (9 Reform Pillars)
    for _, r in df_policy.iterrows():
        cypher_pol = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2016})
            MERGE (pol:StrategicPolicy {record_id: $rec_id})
            SET pol.pillar = $pillar,
                pol.metric_value = $val,
                pol.baseline_2015 = $base,
                pol.yoy_change = $yoy,
                pol.policy_context = $ctx,
                pol.year = 2016
            MERGE (inst)-[:IMPLEMENTED_REFORM]->(pol)
            MERGE (pol)-[:IN_YEAR]->(y)
        """
        s.run(cypher_pol, {
            "rec_id": str(r["record_id"]),
            "pillar": str(r["pillar"]),
            "val": str(r["metric_value"]),
            "base": str(r["baseline_2015"]),
            "yoy": str(r["yoy_change"]),
            "ctx": str(r["policy_context"])
        })
    print(f" - Ingested {len(df_policy)} Strategic Policy records.")

    # 6. Verification Report
    print("\n=== VERIFICATION: FULL 2016 GRAPH ENTITIES ===")
    r_counts = s.run("""
        MATCH (n) WHERE n.year = 2016 OR (n:ReportingYear AND n.year = 2016)
        RETURN labels(n)[0] AS Entity, count(*) AS Count
        ORDER BY Count DESC
    """)
    for row in r_counts:
        print(f" Entity: {row['Entity']:<25} | Count: {row['Count']}")

    r_jur = s.run("""
        MATCH (j:Jurisdiction)-[:RECORDED_CASELOAD]->(jc:JurisdictionCaseload {year: 2016})
        RETURN j.name AS Jurisdiction, jc.total_caseload AS Workload, jc.disposed_cases AS Disposed, jc.disposal_rate_pct AS Rate
        ORDER BY jc.total_caseload DESC
    """)
    print("\n=== 2016 TRIAL JURISDICTIONS IN GRAPH ===")
    for row in r_jur:
        print(f" {row['Jurisdiction'][:35]:<35} | Workload: {row['Workload']:<10} | Putus: {row['Disposed']:<10} | {row['Rate']}%")

driver.close()
print("\n--> Full 2016 Neo4j Ingestion Completed Successfully!")
