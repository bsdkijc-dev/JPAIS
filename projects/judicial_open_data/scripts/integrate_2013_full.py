import os
import json
import hashlib
import subprocess
import pandas as pd
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.http import models

base_dir = os.path.expanduser("~/JPAIS")
proc_dir = os.path.join(base_dir, "data/open_data_2025/processed")
meta_dir = os.path.join(base_dir, "data/open_data_2025/metadata")
pkg_dir = os.path.join(base_dir, "projects/judicial_open_data/release_package/kaggle_dataset")

os.makedirs(proc_dir, exist_ok=True)
os.makedirs(meta_dir, exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "data"), exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "metadata"), exist_ok=True)

# -------------------------------------------------------------
# 1. STRUCTURE FY 2013 DATASET (KPI & METADATA)
# Source: 2013 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Dashboard_Index)
# -------------------------------------------------------------
records_2013 = [
    # Metadata Attributes
    {"record_id": "MA-2013-META-01", "reporting_year": 2013, "domain": "Governance & Lineage", "indicator_name": "Institution", "value": "Mahkamah Agung Republik Indonesia", "baseline_2012": "Mahkamah Agung RI", "yoy_change": "Apex Court", "source_reference": "Official 2013 Annual Report"},
    {"record_id": "MA-2013-META-02", "reporting_year": 2013, "domain": "Governance & Lineage", "indicator_name": "Reporting Period", "value": "1 January 2013 – 31 December 2013", "baseline_2012": "FY 2012", "yoy_change": "Pre-pandemic", "source_reference": "Annual Reporting Cycle"},
    {"record_id": "MA-2013-META-03", "reporting_year": 2013, "domain": "Governance & Lineage", "indicator_name": "Primary Source Document", "value": "Laporan Tahunan 2013 Mahkamah Agung RI", "baseline_2012": "Laptah 2012", "yoy_change": "Official Release Feb 2014", "source_reference": "PDF Verified"},

    # Caseload Productivity (Supreme Court)
    {"record_id": "MA-2013-CASE-01", "reporting_year": 2013, "domain": "Caseload Productivity", "indicator_name": "Total MA Caseload (Beban Perkara MA)", "value": 22449, "baseline_2012": 21107, "yoy_change": "+6.36%", "source_reference": "Part 1, p. 17, Tabel 1"},
    {"record_id": "MA-2013-CASE-02", "reporting_year": 2013, "domain": "Caseload Productivity", "indicator_name": "MA Incoming Cases (Perkara Masuk MA)", "value": 12337, "baseline_2012": 13412, "yoy_change": "-8.02%", "source_reference": "Part 1, p. 17, Tabel 1"},
    {"record_id": "MA-2013-CASE-03", "reporting_year": 2013, "domain": "Caseload Productivity", "indicator_name": "MA Disposed Cases (Perkara Putus MA)", "value": 16034, "baseline_2012": 10995, "yoy_change": "+45.83%", "source_reference": "Part 1, p. 19, Tabel 3"},
    {"record_id": "MA-2013-CASE-04", "reporting_year": 2013, "domain": "Caseload Productivity", "indicator_name": "MA Ending Backlog (Sisa Perkara MA)", "value": 6415, "baseline_2012": 10112, "yoy_change": "-36.56%", "source_reference": "Part 1, p. 19, Tabel 3"},
    {"record_id": "MA-2013-CASE-05", "reporting_year": 2013, "domain": "Caseload Productivity", "indicator_name": "MA Productivity Ratio (Rasio Putus)", "value": "71.42%", "baseline_2012": "52.09%", "yoy_change": "+19.33%", "source_reference": "Part 1, p. 19, Tabel 3"},
    {"record_id": "MA-2013-CASE-06", "reporting_year": 2013, "domain": "Caseload Productivity", "indicator_name": "MA Clearance Rate (Minutasi / Masuk)", "value": "100.19%", "baseline_2012": "93.42%", "yoy_change": "+6.77%", "source_reference": "Part 1, p. 44, Section C.b"},
    {"record_id": "MA-2013-CASE-07", "reporting_year": 2013, "domain": "Judicial Speed", "indicator_name": "Cases Decided < 1 Year (MA)", "value": 6541, "baseline_2012": "Not Reported", "yoy_change": "40.79% of Decisions", "source_reference": "Part 1, p. 46, Tabel 30"},

    # Access to Justice
    {"record_id": "MA-2013-A2J-01", "reporting_year": 2013, "domain": "Access to Justice", "indicator_name": "Religious Court Circuit Hearings (Sidang Keliling PA)", "value": 19383, "baseline_2012": 23675, "yoy_change": "433 Locations (Target: 285)", "source_reference": "Part 2, p. 87, Tabel 2-2"},
    {"record_id": "MA-2013-A2J-02", "reporting_year": 2013, "domain": "Access to Justice", "indicator_name": "Religious Court Fee Waivers (Prodeo PA)", "value": 10252, "baseline_2012": 12243, "yoy_change": "112.02% vs Target (9,152)", "source_reference": "Part 2, p. 89, Tabel 2-4"},
    {"record_id": "MA-2013-A2J-03", "reporting_year": 2013, "domain": "Access to Justice", "indicator_name": "General Court Remote Sessions (Zittingplaats PN)", "value": 3164, "baseline_2012": "Not Reported", "yoy_change": "23 Locations Achieved", "source_reference": "Part 2, p. 86, Tabel 2-1"},

    # Human Resources & Workforce
    {"record_id": "MA-2013-HR-01", "reporting_year": 2013, "domain": "Human Resources", "indicator_name": "Total Judicial Personnel (MA & 4 Jurisdictions)", "value": 33794, "baseline_2012": 34652, "yoy_change": "-2.48%", "source_reference": "Part 4, p. 143, Tabel 4-5"},
    {"record_id": "MA-2013-HR-02", "reporting_year": 2013, "domain": "Human Resources", "indicator_name": "Total Certified Judges (Hakim)", "value": 7708, "baseline_2012": 7867, "yoy_change": "-2.02%", "source_reference": "Part 4, p. 146, Tabel 4-9"},
    {"record_id": "MA-2013-HR-03", "reporting_year": 2013, "domain": "Human Resources", "indicator_name": "Female Workforce Representation (%)", "value": "23.92%", "baseline_2012": "Not Reported", "yoy_change": "8,085 female personnel", "source_reference": "Part 4, p. 145, Tabel 4-7"},

    # Financial & State Revenue Recovery
    {"record_id": "MA-2013-FIN-01", "reporting_year": 2013, "domain": "Financial Execution", "indicator_name": "Final Budget Allocation (Pagu Akhir 2013)", "value": 7254931337000, "baseline_2012": 5057632608000, "yoy_change": "+43.44%", "source_reference": "Part 4, p. 159, Tabel 4-21"},
    {"record_id": "MA-2013-FIN-02", "reporting_year": 2013, "domain": "Financial Execution", "indicator_name": "Budget Realization Rate (%)", "value": "91.60%", "baseline_2012": "95.07%", "yoy_change": "Rp 6.645T Realized", "source_reference": "Part 4, p. 177, Tabel 4-24"},
    {"record_id": "MA-2013-REC-01", "reporting_year": 2013, "domain": "State Revenue Recovery", "indicator_name": "Criminal Fines Imposed (Denda Perkara MA)", "value": 847929700000, "baseline_2012": "Not Reported", "yoy_change": "Asset Recovery", "source_reference": "Part 1, p. 56, Tabel 44"},
    {"record_id": "MA-2013-REC-02", "reporting_year": 2013, "domain": "State Revenue Recovery", "indicator_name": "Restitution / Compensation (Uang Pengganti MA)", "value": 712286515400, "baseline_2012": "Not Reported", "yoy_change": "Asset Recovery", "source_reference": "Part 1, p. 56, Tabel 44"},
    {"record_id": "MA-2013-REC-03", "reporting_year": 2013, "domain": "State Revenue Recovery", "indicator_name": "Non-Tax State Revenue (PNBP Disetor)", "value": 48619148781, "baseline_2012": "Not Reported", "yoy_change": "Treasury Remittance", "source_reference": "Part 4, p. 171, Rekapitulasi"}
]

df_2013 = pd.DataFrame(records_2013)

# Export individual CSV
csv_2013_path = os.path.join(proc_dir, "master_judiciary_open_data_2013.csv")
df_2013.to_csv(csv_2013_path, index=False, encoding="utf-8")
df_2013.to_csv(os.path.join(pkg_dir, "data/master_judiciary_open_data_2013.csv"), index=False, encoding="utf-8")
df_2013.to_csv(os.path.join(pkg_dir, "metadata/master_judiciary_open_data_2013.csv"), index=False, encoding="utf-8")
print(f"--> FY 2013 Dataset exported to: {csv_2013_path}")

# -------------------------------------------------------------
# 2. BUILD THE UNIFIED 13-YEAR MASTER EXCEL (2013-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2013_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_2013.to_excel(writer, sheet_name="OpenData_2013", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2014.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2014.csv")).to_excel(writer, sheet_name="Audit_Register_2014", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2015.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2015.csv")).to_excel(writer, sheet_name="Audit_Register_2015", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_chambers_performance_2016.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_chambers_performance_2016.csv")).to_excel(writer, sheet_name="Chambers_2016", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_jurisdictions_caseload_2016.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_jurisdictions_caseload_2016.csv")).to_excel(writer, sheet_name="Jurisdictions_2016", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2016.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2016.csv")).to_excel(writer, sheet_name="Strategic_2016", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2017.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2017.csv")).to_excel(writer, sheet_name="Audit_Register_2017", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2017.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2017.csv")).to_excel(writer, sheet_name="Strategic_2017", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2018.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2018.csv")).to_excel(writer, sheet_name="Audit_Register_2018", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2019.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2019.csv")).to_excel(writer, sheet_name="Audit_Register_2019", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2019.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2019.csv")).to_excel(writer, sheet_name="OpenData_2019", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2020.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2020.csv")).to_excel(writer, sheet_name="Audit_Register_2020", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_caseload_2021.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_caseload_2021.csv")).to_excel(writer, sheet_name="Caseload_2021", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2021.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_strategic_indicators_2021.csv")).to_excel(writer, sheet_name="Strategic_2021", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2022.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2022.csv")).to_excel(writer, sheet_name="Audit_Register_2022", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2023.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2023.csv")).to_excel(writer, sheet_name="Audit_Register_2023", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")).to_excel(writer, sheet_name="OpenData_2024", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")).to_excel(writer, sheet_name="Master_Taxonomy_2025", index=False)
    if os.path.exists(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")).to_excel(writer, sheet_name="Longitudinal_2021_2025", index=False)

print(f"--> Unified 13-Year Master Excel (2013-2025) generated at: {excel_path}")

# -------------------------------------------------------------
# 3. INGEST FY 2013 INTO NEO4J & QDRANT
# -------------------------------------------------------------
qc = QdrantClient(url="http://127.0.0.1:6333")
q_points = []
p_id = 5000

for _, r in df_2013.iterrows():
    text_repr = f"Tahun 2013 | {r['domain']} | {r['indicator_name']}: {r['value']} (Ref: {r['source_reference']})"
    h = hashlib.sha256(text_repr.encode('utf-8')).digest()
    v = [(b / 255.0) for b in h] * 24
    q_points.append(models.PointStruct(
        id=p_id,
        vector=v[:768],
        payload={"year": 2013, "domain": r["domain"], "indicator": r["indicator_name"], "value": str(r["value"]), "file": "master_judiciary_open_data_2013.csv", "text": text_repr}
    ))
    p_id += 1

qc.upsert(collection_name="court_transparency", points=q_points)
print(f"--> Ingested {len(q_points)} vector points for FY 2013 into Qdrant.")

# Neo4j Ingestion
driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=('neo4j', 'JpaisLegalGraph2026!'))
with driver.session() as s:
    s.run("""
        MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})
        MERGE (y:ReportingYear {year: 2013})
        MERGE (src:SourceDocument {name: 'Laporan Tahunan 2013 Mahkamah Agung RI', publication_year: 2014})
        MERGE (inst)-[:PUBLISHED]->(src)
        MERGE (src)-[:COVERS_YEAR]->(y)
    """)

    for _, r in df_2013.iterrows():
        cypher = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2013})
            MERGE (item:AuditProperty {record_id: $rec_id})
            SET item.domain = $domain,
                item.indicator_name = $name,
                item.value = $val,
                item.baseline_2012 = $base,
                item.yoy_change = $yoy,
                item.reference = $ref,
                item.year = 2013
            MERGE (inst)-[:HAS_AUDIT_RECORD]->(item)
            MERGE (item)-[:IN_YEAR]->(y)
        """
        s.run(cypher, {
            "rec_id": str(r["record_id"]),
            "domain": str(r["domain"]),
            "name": str(r["indicator_name"]),
            "val": str(r["value"]),
            "base": str(r["baseline_2012"]),
            "yoy": str(r["yoy_change"]),
            "ref": str(r["source_reference"])
        })
print("--> Ingested 2013 Audit Entities and Relationships into Neo4j.")
driver.close()
