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
# 1. STRUCTURE FY 2012 DATASET (METADATA & CHAPTERS)
# Source: 2012 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Source_Audit_Register)
# -------------------------------------------------------------
records_2012 = [
    # Document Identity
    {"record_id": "MA-2012-DOC-01", "reporting_year": 2012, "section_type": "Document Identity", "item_code": "DOC-01", "attribute": "Document Title", "terminology_id": "Judul Dokumen", "value": "Laporan Tahunan 2012 Mahkamah Agung Republik Indonesia", "source_reference": "Cover & Title Page (p. 1-3)", "status": "VERIFIED", "notes": "Official institutional annual report of the Supreme Court"},
    {"record_id": "MA-2012-DOC-02", "reporting_year": 2012, "section_type": "Document Identity", "item_code": "DOC-02", "attribute": "Publishing Institution", "terminology_id": "Lembaga Penerbit", "value": "Mahkamah Agung Republik Indonesia", "source_reference": "Title Page (p. 3)", "status": "VERIFIED", "notes": "Apex judicial authority of Indonesia"},
    {"record_id": "MA-2012-DOC-03", "reporting_year": 2012, "section_type": "Document Identity", "item_code": "DOC-03", "attribute": "Reporting Period", "terminology_id": "Periode Pelaporan", "value": "1 Januari 2012 - 31 Desember 2012", "source_reference": "Executive Summary (p. 31)", "status": "VERIFIED", "notes": "Covers full fiscal & judicial reporting calendar 2012"},
    {"record_id": "MA-2012-DOC-04", "reporting_year": 2012, "section_type": "Document Identity", "item_code": "DOC-04", "attribute": "Publication Date", "terminology_id": "Waktu Penerbitan", "value": "Maret 2013", "source_reference": "Cover Page (p. 1)", "status": "VERIFIED", "notes": "Formally published in Jakarta, March 2013"},
    {"record_id": "MA-2012-DOC-05", "reporting_year": 2012, "section_type": "Document Identity", "item_code": "DOC-05", "attribute": "Document Scope", "terminology_id": "Cakupan Kelembagaan", "value": "Mahkamah Agung RI & 4 Lingkungan Peradilan", "source_reference": "Structure (p. 8-9)", "status": "VERIFIED", "notes": "Includes General, Religious, Military & State Administrative courts"},
    {"record_id": "MA-2012-DOC-06", "reporting_year": 2012, "section_type": "Document Identity", "item_code": "DOC-06", "attribute": "Document Extent", "terminology_id": "Jumlah Halaman PDF", "value": "321 Halaman", "source_reference": "PDF Document Index", "status": "VERIFIED", "notes": "Total verified pages in official publication PDF"},
    {"record_id": "MA-2012-DOC-07", "reporting_year": 2012, "section_type": "Leadership", "item_code": "DOC-07", "attribute": "Chief Justice (KMA)", "terminology_id": "Ketua Mahkamah Agung", "value": "Dr. H.M. Hatta Ali, S.H., M.H.", "source_reference": "Profile & Preface (p. 4, 11)", "status": "VERIFIED", "notes": "13th Chief Justice of MA RI, elected February 2012"},
    {"record_id": "MA-2012-DOC-08", "reporting_year": 2012, "section_type": "Leadership", "item_code": "DOC-08", "attribute": "Vice CJ - Judicial", "terminology_id": "Wakil Ketua Bidang Yudisial", "value": "H. Abdul Kadir Mappong, S.H.", "source_reference": "Leadership Profile (p. 10)", "status": "VERIFIED", "notes": "Oversees judicial technical operations & chamber performance"},
    {"record_id": "MA-2012-DOC-09", "reporting_year": 2012, "section_type": "Leadership", "item_code": "DOC-09", "attribute": "Vice CJ - Non Judicial", "terminology_id": "Wakil Ketua Non-Yudisial", "value": "Dr. H. Ahmad Kamil, S.H., M.Hum.", "source_reference": "Leadership Profile (p. 10)", "status": "VERIFIED", "notes": "Oversees court administration, finance, HR & assets"},
    {"record_id": "MA-2012-DOC-10", "reporting_year": 2012, "section_type": "Strategic Reform", "item_code": "DOC-10", "attribute": "Strategic Mandate", "terminology_id": "Mandat & Reformasi", "value": "Cetak Biru 2010-2035 & Implementasi Sistem Kamar", "source_reference": "Blueprint Mandate (p. 37, 65)", "status": "VERIFIED", "notes": "Year 3 of judicial reform blueprint; Year 1 of chamber system"},

    # Chapter Inventory
    {"record_id": "MA-2012-CH-01", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-01", "attribute": "Bagian Pertama: Manajemen Perkara", "terminology_id": "Case Management", "value": "p. 63-88", "source_reference": "p. 63-88", "status": "VERIFIED", "notes": "Caseload, Kasasi, PK, Grasi, HUM, Clearance Rate, Chamber System"},
    {"record_id": "MA-2012-CH-02", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-02", "attribute": "Bagian Kedua: Akses Terhadap Keadilan", "terminology_id": "Access to Justice", "value": "p. 89-110", "source_reference": "p. 89-110", "status": "VERIFIED", "notes": "Posbakum, Prodeo, Sidang Keliling, One-Day Publish, Direktori Putusan"},
    {"record_id": "MA-2012-CH-03", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-03", "attribute": "Bagian Ketiga: Pengawasan Internal", "terminology_id": "Internal Supervision", "value": "p. 111-140", "source_reference": "p. 111-140", "status": "VERIFIED", "notes": "Public complaints, Disciplinary sanctions, MKH, BPK & BPKP audits"},
    {"record_id": "MA-2012-CH-04", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-04", "attribute": "Bagian Keempat: Manajemen SDM, Anggaran & Aset", "terminology_id": "HR, Finance & Asset Mgt", "value": "p. 141-220", "source_reference": "p. 141-220", "status": "VERIFIED", "notes": "Personnel demographics, DIPA APBN-P, PNBP revenue, BMN inventory"},
    {"record_id": "MA-2012-CH-05", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-05", "attribute": "Bagian Kelima: Penelitian, Pengembangan & Diklat", "terminology_id": "Research, Dev & Training", "value": "p. 221-252", "source_reference": "p. 221-252", "status": "VERIFIED", "notes": "PPC Terpadu Cakim VI/VII, CJE II, Certification, Research reports"},
    {"record_id": "MA-2012-CH-06", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-06", "attribute": "Bagian Keenam: Reformasi Birokrasi", "terminology_id": "Bureaucratic Reform", "value": "p. 253-258", "source_reference": "p. 253-258", "status": "VERIFIED", "notes": "TQA BPKP evaluation (Score 70.59 / Cukup), 8 Areas of Change"},
    {"record_id": "MA-2012-CH-07", "reporting_year": 2012, "section_type": "Chapter Inventory", "item_code": "CH-07", "attribute": "Bagian Ketujuh & Delapan: Kerjasama & Landmark", "terminology_id": "International & Landmark", "value": "p. 259-310", "source_reference": "p. 259-310", "status": "VERIFIED", "notes": "Bilateral judicial cooperation (FCA Australia), Landmark decisions"}
]

df_2012 = pd.DataFrame(records_2012)

# Export individual CSV
csv_2012_path = os.path.join(proc_dir, "source_audit_register_2012.csv")
df_2012.to_csv(csv_2012_path, index=False, encoding="utf-8")
df_2012.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2012.csv"), index=False, encoding="utf-8")
df_2012.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2012.csv"), index=False, encoding="utf-8")
print(f"--> FY 2012 Dataset exported to: {csv_2012_path}")

# -------------------------------------------------------------
# 2. BUILD THE UNIFIED 14-YEAR MASTER EXCEL (2012-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2012_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_2012.to_excel(writer, sheet_name="Audit_Register_2012", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2013.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2013.csv")).to_excel(writer, sheet_name="OpenData_2013", index=False)
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

print(f"--> Unified 14-Year Master Excel (2012-2025) generated at: {excel_path}")

# -------------------------------------------------------------
# 3. INGEST FY 2012 INTO NEO4J & QDRANT
# -------------------------------------------------------------
qc = QdrantClient(url="http://127.0.0.1:6333")
q_points = []
p_id = 6000

for _, r in df_2012.iterrows():
    text_repr = f"Tahun 2012 | {r['section_type']} | {r['attribute']}: {r['value']} (Ref: {r['source_reference']})"
    h = hashlib.sha256(text_repr.encode('utf-8')).digest()
    v = [(b / 255.0) for b in h] * 24
    q_points.append(models.PointStruct(
        id=p_id,
        vector=v[:768],
        payload={"year": 2012, "section": r["section_type"], "attribute": r["attribute"], "value": r["value"], "file": "source_audit_register_2012.csv", "text": text_repr}
    ))
    p_id += 1

qc.upsert(collection_name="court_transparency", points=q_points)
print(f"--> Ingested {len(q_points)} vector points for FY 2012 into Qdrant.")

# Neo4j Ingestion
driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=('neo4j', 'JpaisLegalGraph2026!'))
with driver.session() as s:
    s.run("""
        MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})
        MERGE (y:ReportingYear {year: 2012})
        MERGE (src:SourceDocument {name: 'Laporan Tahunan 2012 Mahkamah Agung Republik Indonesia', publication_date: '2013-03-01', total_pages: 321})
        MERGE (inst)-[:PUBLISHED]->(src)
        MERGE (src)-[:COVERS_YEAR]->(y)
    """)

    for _, r in df_2012.iterrows():
        cypher = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2012})
            MERGE (item:AuditProperty {record_id: $rec_id})
            SET item.code = $code,
                item.section_type = $sec,
                item.attribute = $attr,
                item.terminology_id = $term_id,
                item.value = $val,
                item.reference = $ref,
                item.notes = $notes,
                item.year = 2012
            MERGE (inst)-[:HAS_AUDIT_RECORD]->(item)
            MERGE (item)-[:IN_YEAR]->(y)
        """
        s.run(cypher, {
            "rec_id": str(r["record_id"]),
            "code": str(r["item_code"]),
            "sec": str(r["section_type"]),
            "attr": str(r["attribute"]),
            "term_id": str(r["terminology_id"]),
            "val": str(r["value"]),
            "ref": str(r["source_reference"]),
            "notes": str(r["notes"])
        })
print("--> Ingested 2012 Audit Entities and Relationships into Neo4j.")
driver.close()
