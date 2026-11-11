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
# 1. STRUCTURE FY 2014 SOURCE AUDIT REGISTER
# Source: 2014 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A1:G15)
# -------------------------------------------------------------
records_2014 = [
    # Document Identity
    {"record_id": "MA-2014-DOC-01", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_TITLE", "title_id": "Judul Dokumen", "title_en": "Document Title", "value": "Laporan Tahunan 2014 Mahkamah Agung Republik Indonesia", "pages": "Cover", "scope": "Official Annual Report", "status": "VERIFIED"},
    {"record_id": "MA-2014-DOC-02", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_PUB", "title_id": "Penerbit", "title_en": "Publisher", "value": "Mahkamah Agung Republik Indonesia", "pages": "Imprint", "scope": "Central Administration", "status": "VERIFIED"},
    {"record_id": "MA-2014-DOC-03", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_PERIOD", "title_id": "Periode Pelaporan", "title_en": "Reporting Period", "value": "1 Januari 2014 – 31 Desember 2014", "pages": "Overview", "scope": "FY 2014 Pre-Pandemic", "status": "VERIFIED"},
    {"record_id": "MA-2014-DOC-04", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_DATE", "title_id": "Tanggal Publikasi", "title_en": "Publication Date", "value": "17 Maret 2015 (Jakarta)", "pages": "Sekapur Sirih", "scope": "Official Release Date", "status": "VERIFIED"},
    {"record_id": "MA-2014-DOC-05", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_PAGES", "title_id": "Jumlah Halaman", "title_en": "Total Document Pages", "value": "382 Pages", "pages": "1-382", "scope": "Verified Pagination", "status": "VERIFIED"},
    {"record_id": "MA-2014-DOC-06", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_FILE_ID", "title_id": "ID Berkas Sumber", "title_en": "Source File ID", "value": "1YuB5_SIijMNsOGHPPniJqPIyMNPPLLBa", "pages": "Drive Ref", "scope": "Digital Archive Master", "status": "VERIFIED"},
    {"record_id": "MA-2014-DOC-07", "reporting_year": 2014, "section_type": "Document Identity", "item_code": "DOC_SCOPE", "title_id": "Cakupan Data", "title_en": "Data Scope", "value": "Supreme Court (Mahkamah Agung) & 4 Judicial Jurisdictions", "pages": "TOC", "scope": "Umum, Agama, Militer, TUN, Pajak", "status": "VERIFIED"},

    # Chapter Inventory
    {"record_id": "MA-2014-CH-00", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH00", "title_id": "Profil & Unsur Pimpinan MA RI", "title_en": "Executive Profile & Judicial Leadership", "value": "i-xx (1-20)", "pages": "pp. 1-20", "scope": "Visi/Misi, Pimpinan MA, Hakim Agung, Eselon 1", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-01", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH01", "title_id": "Bagian Pertama: Manajemen Perkara", "title_en": "Part 1: Case Management & Adjudication", "value": "1-106 (23-128)", "pages": "pp. 23-128", "scope": "Agenda Pembaruan, Sistem Kamar, Kasasi, PK, Sisa, Minutasi", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-02", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH02", "title_id": "Bagian Kedua: Akses Terhadap Keadilan", "title_en": "Part 2: Access to Justice & Public Services", "value": "107-130 (129-152)", "pages": "pp. 129-152", "scope": "PERMA 1/2014, Pembebasan Biaya, Posbakum, Sidang Keliling", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-03", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH03", "title_id": "Bagian Ketiga: Pengawasan Internal", "title_en": "Part 3: Internal Oversight & Integrity", "value": "131-160 (153-182)", "pages": "pp. 153-182", "scope": "Audit Kinerja/Integritas, Sidak, MKH, Disiplin Aparatur", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-04", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH04", "title_id": "Bagian Keempat: Manajemen SDM, Anggaran & Aset", "title_en": "Part 4: Workforce, Financials & Asset Management", "value": "161-242 (183-264)", "pages": "pp. 183-264", "scope": "Formasi CPNS, Profil Hakim/PNS, DIPA, BMN, WTP BPK", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-05", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH05", "title_id": "Bagian Kelima: Balitbang Diklat Kumdil", "title_en": "Part 5: Judicial Research & Professional Training", "value": "243-264 (265-286)", "pages": "pp. 265-286", "scope": "Penelitian, ISO 9001:2008 Pusdiklat Menpim, Diklat Teknis", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-06", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH06", "title_id": "Bagian Keenam: Forum Internasional", "title_en": "Part 6: International Judicial Engagement", "value": "265-286 (287-308)", "pages": "pp. 287-308", "scope": "Kerjasama Bilateral, Konferensi Lingkungan ASEAN", "status": "VERIFIED"},
    {"record_id": "MA-2014-CH-07", "reporting_year": 2014, "section_type": "Chapter Inventory", "item_code": "CH07", "title_id": "Bagian Ketujuh: Landmark Decisions & SK", "title_en": "Part 7: Landmark Decisions & Decrees", "value": "287-382 (309-382)", "pages": "pp. 309-382", "scope": "Putusan Penting (Landmark), SK Pokja Laptah 2014", "status": "VERIFIED"}
]

df_2014 = pd.DataFrame(records_2014)

# Export individual CSV
csv_2014_path = os.path.join(proc_dir, "source_audit_register_2014.csv")
df_2014.to_csv(csv_2014_path, index=False, encoding="utf-8")
df_2014.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2014.csv"), index=False, encoding="utf-8")
df_2014.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2014.csv"), index=False, encoding="utf-8")
print(f"--> FY 2014 Dataset exported to: {csv_2014_path}")

# -------------------------------------------------------------
# 2. BUILD THE UNIFIED 12-YEAR MASTER EXCEL (2014-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2014_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_2014.to_excel(writer, sheet_name="Audit_Register_2014", index=False)
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

print(f"--> Unified 12-Year Master Excel (2014-2025) generated at: {excel_path}")

# -------------------------------------------------------------
# 3. INGEST FY 2014 INTO NEO4J & QDRANT
# -------------------------------------------------------------
# Qdrant Ingestion
qc = QdrantClient(url="http://127.0.0.1:6333")
q_points = []
p_id = 4000

for _, r in df_2014.iterrows():
    text_repr = f"Tahun 2014 | {r['section_type']} | {r['title_en']}: {r['value']} (Scope: {r['scope']})"
    h = hashlib.sha256(text_repr.encode('utf-8')).digest()
    v = [(b / 255.0) for b in h] * 24
    q_points.append(models.PointStruct(
        id=p_id,
        vector=v[:768],
        payload={"year": 2014, "section": r["section_type"], "item": r["title_en"], "value": r["value"], "file": "source_audit_register_2014.csv", "text": text_repr}
    ))
    p_id += 1

qc.upsert(collection_name="court_transparency", points=q_points)
print(f"--> Ingested {len(q_points)} vector points for FY 2014 into Qdrant.")

# Neo4j Ingestion
driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=('neo4j', 'JpaisLegalGraph2026!'))
with driver.session() as s:
    s.run("""
        MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})
        MERGE (y:ReportingYear {year: 2014})
        MERGE (src:SourceDocument {name: 'Laporan Tahunan 2014 Mahkamah Agung RI', publication_date: '2015-03-17', total_pages: 382})
        MERGE (inst)-[:PUBLISHED]->(src)
        MERGE (src)-[:COVERS_YEAR]->(y)
    """)

    for _, r in df_2014.iterrows():
        cypher = """
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (y:ReportingYear {year: 2014})
            MERGE (item:AuditProperty {record_id: $rec_id})
            SET item.code = $code,
                item.section_type = $sec,
                item.title_id = $t_id,
                item.title_en = $t_en,
                item.value = $val,
                item.pages = $pages,
                item.scope = $scope,
                item.year = 2014
            MERGE (inst)-[:HAS_AUDIT_RECORD]->(item)
            MERGE (item)-[:IN_YEAR]->(y)
        """
        s.run(cypher, {
            "rec_id": str(r["record_id"]),
            "code": str(r["item_code"]),
            "sec": str(r["section_type"]),
            "t_id": str(r["title_id"]),
            "t_en": str(r["title_en"]),
            "val": str(r["value"]),
            "pages": str(r["pages"]),
            "scope": str(r["scope"])
        })
print("--> Ingested 2014 Audit Entities and Relationships into Neo4j.")
driver.close()
