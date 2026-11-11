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
# 1. STRUCTURE FY 2015 SOURCE AUDIT DATASET
# Source: 2015 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A1:G16)
# -------------------------------------------------------------
records_2015 = [
    # Document Identity
    {"record_id": "MA-2015-DOC-01", "reporting_year": 2015, "category": "Document Identity", "attribute": "Document Title", "specification": "Official Annual Report of the Supreme Court of Indonesia", "value": "Laporan Tahunan 2015 Mahkamah Agung RI", "source_reference": "Page 1-2 (Cover, Copyright)", "verification_status": "VERIFIED", "notes": "Official PDF (392 pages)"},
    {"record_id": "MA-2015-DOC-02", "reporting_year": 2015, "category": "Document Identity", "attribute": "Publisher & ISBN", "specification": "Pokja Laporan Tahunan Mahkamah Agung RI", "value": "ISBN: 978-979-8512-89-6", "source_reference": "Page 2, Cetakan I Feb 2016", "verification_status": "VERIFIED", "notes": "Medan Merdeka Utara 9-13"},
    {"record_id": "MA-2015-DOC-03", "reporting_year": 2015, "category": "Document Identity", "attribute": "Reporting Period", "specification": "Temporal Coverage", "value": "1 Jan 2015 - 31 Des 2015", "source_reference": "Page xviii, 15", "verification_status": "VERIFIED", "notes": "Pre-Pandemic Baseline"},
    {"record_id": "MA-2015-DOC-04", "reporting_year": 2015, "category": "Document Identity", "attribute": "Institutional Leadership", "specification": "Ketua Mahkamah Agung RI", "value": "Prof. Dr. M. Hatta Ali, S.H., M.H.", "source_reference": "Page x, xx (1 Maret 2016)", "verification_status": "VERIFIED", "notes": "Chief Justice Term"},
    {"record_id": "MA-2015-DOC-05", "reporting_year": 2015, "category": "Document Identity", "attribute": "Data Classification", "specification": "Public Open Data Infrastructure", "value": "PUBLIC / UNRESTRICTED", "source_reference": "SK KMA 1-144/KMA/SK/I/2011", "verification_status": "VERIFIED", "notes": "Research-Ready Open Data"},

    # Chapter Mapping & Scope
    {"record_id": "MA-2015-SEC-01", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian I: Case Management & Judicial Productivity", "specification": "Manajemen Perkara", "value": "Hal. 1 - 80 (PDF 33-112)", "source_reference": "Hal. 1-80", "verification_status": "VERIFIED", "notes": "DS01 & DS04: Caseload, Clearance Rate, Processing Time, Fines"},
    {"record_id": "MA-2015-SEC-02", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian II: Bureaucratic Reform & Governance", "specification": "Reformasi Birokrasi", "value": "Hal. 81 - 102 (PDF 113-134)", "source_reference": "Hal. 81-102", "verification_status": "VERIFIED", "notes": "DS14: PMPRB, Integrity Zone, SOP, SAKIP"},
    {"record_id": "MA-2015-SEC-03", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian III: Access to Justice & Public Services", "specification": "Akses Terhadap Keadilan", "value": "Hal. 103 - 124 (PDF 135-156)", "source_reference": "Hal. 103-124", "verification_status": "VERIFIED", "notes": "DS07: Posbakum, Prodeo, Circuit Courts, ATR, E-SKUM"},
    {"record_id": "MA-2015-SEC-04", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian IV: Judicial Oversight & Discipline", "specification": "Pengawasan", "value": "Hal. 125 - 148 (PDF 157-180)", "source_reference": "Hal. 125-148", "verification_status": "VERIFIED", "notes": "DS13: Hukuman Disiplin, MKH, SPI, Audit Kinerja"},
    {"record_id": "MA-2015-SEC-05", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian V: Human Resource Management", "specification": "Manajemen Sumber Daya Manusia", "value": "Hal. 149 - 186 (PDF 181-218)", "source_reference": "Hal. 149-186", "verification_status": "VERIFIED", "notes": "DS11: Judicial Workforce, Gender, Positions, Training"},
    {"record_id": "MA-2015-SEC-06", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian VI: Financial and Asset Management", "specification": "Manajemen Keuangan dan Aset", "value": "Hal. 187 - 262 (PDF 219-262)", "source_reference": "Hal. 187-262", "verification_status": "VERIFIED", "notes": "DS18: Budget Execution, PNBP, Asset Recovery"},
    {"record_id": "MA-2015-SEC-07", "reporting_year": 2015, "category": "Chapter Scope", "attribute": "Bagian VII-IX: Research, International Relations & Precedents", "specification": "Litbang, Kerjasama & Landmark Decisions", "value": "Hal. 263 - 364 (PDF 263-364)", "source_reference": "Hal. 263-364", "verification_status": "VERIFIED", "notes": "DS19 & DS20: Legal research, ACJM, Jurisprudence"}
]

df_2015 = pd.DataFrame(records_2015)

# Export individual CSVs
csv_2015_path = os.path.join(proc_dir, "source_audit_register_2015.csv")
df_2015.to_csv(csv_2015_path, index=False, encoding="utf-8")
df_2015.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2015.csv"), index=False, encoding="utf-8")
df_2015.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2015.csv"), index=False, encoding="utf-8")
print(f"--> FY 2015 Dataset exported to: {csv_2015_path}")

# -------------------------------------------------------------
# 2. BUILD THE UNIFIED 11-YEAR MASTER EXCEL (2015-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2015_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_2015.to_excel(writer, sheet_name="Audit_Register_2015", index=False)
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

print(f"--> Unified 11-Year Master Excel (2015-2025) generated at: {excel_path}")

# -------------------------------------------------------------
# 3. INGEST FY 2015 INTO NEO4J & QDRANT
# -------------------------------------------------------------
# Qdrant Ingestion
qc = QdrantClient(url="http://127.0.0.1:6333")
q_points = []
p_id = 3000

for _, r in df_2015.iterrows():
    text_repr = f"Tahun 2015 | {r['category']} | {r['attribute']}: {r['value']} (Ref: {r['source_reference']})"
    h = hashlib.sha256(text_repr.encode('utf-8')).digest()
    v = [(b / 255.0) for b in h] * 24
    q_points.append(models.PointStruct(
        id=p_id,
        vector=v[:768],
        payload={"year": 2015, "category": r["category"], "attribute": r["attribute"], "value": r["value"], "file": "source_audit_register_2015.csv", "text": text_repr}
    ))
    p_id += 1

qc.upsert(collection_name="court_transparency", points=q_points)
print(f"--> Ingested {len(q_points)} vector points for FY 2015 into Qdrant.")

# Neo4j Ingestion
driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=('neo4j', 'JpaisLegalGraph2026!'))
with driver.session() as s:
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (sec:ChapterSection) REQUIRE sec.code IS UNIQUE")
    s.run("""
        MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})
        MERGE (y:ReportingYear {year: 2015})
        MERGE (src:SourceDocument {name: 'Laporan Tahunan 2015 Mahkamah Agung RI', publication_year: 2016, isbn: '978-979-8512-89-6', total_pages: 392})
        MERGE (inst)-[:PUBLISHED]->(src)
        MERGE (src)-[:COVERS_YEAR]->(y)
    """)

    for _, r in df_2015.iterrows():
        cypher = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2015})
            MERGE (item:AuditProperty {record_id: $rec_id})
            SET item.attribute = $attr,
                item.value = $val,
                item.category = $cat,
                item.specification = $spec,
                item.reference = $ref,
                item.notes = $notes,
                item.year = 2015
            MERGE (inst)-[:HAS_AUDIT_RECORD]->(item)
            MERGE (item)-[:IN_YEAR]->(y)
        """
        s.run(cypher, {
            "rec_id": str(r["record_id"]),
            "attr": str(r["attribute"]),
            "val": str(r["value"]),
            "cat": str(r["category"]),
            "spec": str(r["specification"]),
            "ref": str(r["source_reference"]),
            "notes": str(r["notes"])
        })
print("--> Ingested 2015 Audit Entities and Relationships into Neo4j.")
driver.close()
