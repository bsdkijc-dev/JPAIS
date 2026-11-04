import os
import pandas as pd
import json

base_dir = os.path.expanduser("~/JPAIS")
proc_dir = os.path.join(base_dir, "data/open_data_2025/processed")
meta_dir = os.path.join(base_dir, "data/open_data_2025/metadata")
pkg_dir = os.path.join(base_dir, "projects/judicial_open_data/release_package/kaggle_dataset")

os.makedirs(proc_dir, exist_ok=True)
os.makedirs(meta_dir, exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "data"), exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "metadata"), exist_ok=True)

# -------------------------------------------------------------
# 1. FY 2019 METADATA AUDIT ATTRIBUTES
# Source: 2019 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A1:E11)
# -------------------------------------------------------------
meta_2019 = [
    {"field_code": "DOC_TITLE", "reporting_year": 2019, "metadata_attribute": "Document Title", "value": "Laporan Tahunan 2019 Mahkamah Agung Republik Indonesia", "citation": "Cover, p. 1-3", "notes": "Official Annual Report"},
    {"field_code": "DOC_PUB", "reporting_year": 2019, "metadata_attribute": "Publisher", "value": "Mahkamah Agung Republik Indonesia", "citation": "Editorial, p. 3", "notes": "ISBN: 978-623-7805-00-7"},
    {"field_code": "DOC_PERIOD", "reporting_year": 2019, "metadata_attribute": "Reporting Period", "value": "1 January 2019 – 31 December 2019", "citation": "Executive Summary, p. 14", "notes": "Pre-pandemic reporting year"},
    {"field_code": "DOC_PUB_YEAR", "reporting_year": 2019, "metadata_attribute": "Publication Year", "value": "2020", "citation": "Foreword, p. 17", "notes": "Published in Jakarta, February 2020"},
    {"field_code": "DOC_LANG", "reporting_year": 2019, "metadata_attribute": "Language", "value": "Bahasa Indonesia", "citation": "Report Text", "notes": "Standardized English metadata lineage"},
    {"field_code": "DOC_CLASS", "reporting_year": 2019, "metadata_attribute": "Data Classification", "value": "PUBLIC (Keterbukaan Informasi Publik)", "citation": "UU 14/2008; p. 14", "notes": "Public institutional release"},
    {"field_code": "INST_SCOPE", "reporting_year": 2019, "metadata_attribute": "Institutional Scope", "value": "Mahkamah Agung RI & 4 Lingkungan Peradilan", "citation": "Organizational Structure, p. 20-21", "notes": "MA, Umum, Agama, Militer, TUN, Pajak"},
    {"field_code": "PAGES_TOTAL", "reporting_year": 2019, "metadata_attribute": "Document Length", "value": "312 Pages", "citation": "PDF Pagination Index", "notes": "Complete audited PDF volume"},
    {"field_code": "BASELINE_YEAR", "reporting_year": 2019, "metadata_attribute": "Comparative Baseline", "value": "2018 (Officially Reported Baselines Only)", "citation": "Comparative Tables (Bab I-IV)", "notes": "Temporal accuracy preserved"}
]

# -------------------------------------------------------------
# 2. FY 2019 20 MASTER DATASET TAXONOMY (DS01 - DS20)
# Source: 2019 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A13:E34)
# -------------------------------------------------------------
taxonomy_2019 = [
    {"dataset_id": "DS01", "reporting_year": 2019, "category": "Judicial Performance", "master_dataset_name": "Case_Distribution", "scope": "Perkara Masuk & Distribusi Perkara", "source_mapping": "Bab I: p. 75-79, 101, 110, 117, 120, 122"},
    {"dataset_id": "DS02", "reporting_year": 2019, "category": "Judicial Performance", "master_dataset_name": "Case_Disposition", "scope": "Perkara Diputus & Produktivitas Putus", "source_mapping": "Bab I: p. 75-80, 84-98, 101-123"},
    {"dataset_id": "DS03", "reporting_year": 2019, "category": "Judicial Performance", "master_dataset_name": "Case_Backlog", "scope": "Sisa Perkara & Tunggakan Akhir Tahun", "source_mapping": "Bab I: p. 62, 75-79, 83, 101, 110"},
    {"dataset_id": "DS04", "reporting_year": 2019, "category": "Judicial Performance", "master_dataset_name": "Case_Processing_Time", "scope": "Rerata Waktu Memutus & Waktu Minutasi", "source_mapping": "Bab I: p. 80-83, 105, 110, 121, 125"},
    {"dataset_id": "DS05", "reporting_year": 2019, "category": "Judicial Performance", "master_dataset_name": "Case_Appeal_and_Review", "scope": "Upaya Hukum Banding, Kasasi, dan PK", "source_mapping": "Bab I: p. 81-83, 123-127"},
    {"dataset_id": "DS06", "reporting_year": 2019, "category": "Judicial Performance", "master_dataset_name": "Court_Performance", "scope": "Clearance Rate & Rasio Kinerja Per Hakim", "source_mapping": "Bab I: p. 80, 84, 128-129"},
    {"dataset_id": "DS07", "reporting_year": 2019, "category": "Access to Justice", "master_dataset_name": "Legal_Aid", "scope": "Pos Bantuan Hukum (Posbakum) Pengadilan", "source_mapping": "Bab II: p. 137, 149-151"},
    {"dataset_id": "DS08", "reporting_year": 2019, "category": "Access to Justice", "master_dataset_name": "Fee_Waiver_and_Prodeo", "scope": "Layanan Pembebasan Biaya Perkara (Prodeo)", "source_mapping": "Bab II: p. 137, 149"},
    {"dataset_id": "DS09", "reporting_year": 2019, "category": "Access to Justice", "master_dataset_name": "Remote_and_Electronic_Court_Services", "scope": "Sidang Luar Gedung, Sidang Keliling, Isbat Luar Negeri", "source_mapping": "Bab II: p. 137, 149-153"},
    {"dataset_id": "DS10", "reporting_year": 2019, "category": "Access to Justice", "master_dataset_name": "Public_Service_and_Complaints", "scope": "PTSP, Meja Informasi, Siwas, dan Pengaduan", "source_mapping": "Bab II: p. 137, 151-154; Bab VI: p. 248-251"},
    {"dataset_id": "DS11", "reporting_year": 2019, "category": "Institutional Governance", "master_dataset_name": "Judicial_Human_Resources", "scope": "Komposisi Hakim, Panitera, Jurusita, & ASN", "source_mapping": "Bab III: p. 160, 164-166"},
    {"dataset_id": "DS12", "reporting_year": 2019, "category": "Institutional Governance", "master_dataset_name": "Judicial_Training_and_Development", "scope": "Pendidikan & Pelatihan Calon Hakim, Sertifikasi", "source_mapping": "Bab III: p. 167-175"},
    {"dataset_id": "DS13", "reporting_year": 2019, "category": "Institutional Governance", "master_dataset_name": "Institutional_Integrity_and_Discipline", "scope": "Hukuman Disiplin, MKH, SMAP ISO 37001", "source_mapping": "Bab II: p. 136; Bab VI: p. 248-255"},
    {"dataset_id": "DS14", "reporting_year": 2019, "category": "Institutional Governance", "master_dataset_name": "Court_Administration_and_Governance", "scope": "Zona Integritas (WBK/WBBM) & Akreditasi APM", "source_mapping": "Bab II: p. 140-147"},
    {"dataset_id": "DS15", "reporting_year": 2019, "category": "Digital Transformation", "master_dataset_name": "Judicial_Digital_Transformation", "scope": "e-Court, e-Litigation, Direktori Putusan", "source_mapping": "Bab I: p. 64-67, 73; Bab II: p. 142-146"},
    {"dataset_id": "DS16", "reporting_year": 2019, "category": "Digital Transformation", "master_dataset_name": "Judicial_Information_Systems", "scope": "SIPP, SIKEP, SIPERMARI, SPPT-TI, Command Center", "source_mapping": "Bab I: p. 74; Bab II: p. 137, 147; Bab III: p. 160"},
    {"dataset_id": "DS17", "reporting_year": 2019, "category": "Digital Transformation", "master_dataset_name": "Data_Transparency_and_Public_Access", "scope": "Publikasi Putusan, Majalah, Jurnal Hukum", "source_mapping": "Bab II: p. 151-156"},
    {"dataset_id": "DS18", "reporting_year": 2019, "category": "Financial & Strategic", "master_dataset_name": "Budget_and_Financial_Performance", "scope": "Pagu Anggaran, Realisasi Belanja, Opini WTP", "source_mapping": "Bab IV: p. 16, 192-202"},
    {"dataset_id": "DS19", "reporting_year": 2019, "category": "Financial & Strategic", "master_dataset_name": "Strategic_Programs_and_KPIs", "scope": "Indikator Kinerja Utama & Capaian PMPRB", "source_mapping": "Bab I: p. 77; Bab II: p. 139-140"},
    {"dataset_id": "DS20", "reporting_year": 2019, "category": "Financial & Strategic", "master_dataset_name": "State_Revenue_and_Financial_Recovery", "scope": "PNBP Fungsional, Eksekusi Denda & Uang Pengganti", "source_mapping": "Bab I: p. 130-131; Bab IV: p. 202-204"}
]

df_meta_2019 = pd.DataFrame(meta_2019)
df_tax_2019 = pd.DataFrame(taxonomy_2019)

# Export individual CSV files
csv_meta_path = os.path.join(proc_dir, "source_audit_register_2019.csv")
csv_tax_path = os.path.join(proc_dir, "master_judiciary_open_data_2019.csv")

df_meta_2019.to_csv(csv_meta_path, index=False, encoding="utf-8")
df_tax_2019.to_csv(csv_tax_path, index=False, encoding="utf-8")

df_meta_2019.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2019.csv"), index=False, encoding="utf-8")
df_meta_2019.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2019.csv"), index=False, encoding="utf-8")
df_tax_2019.to_csv(os.path.join(pkg_dir, "data/master_judiciary_open_data_2019.csv"), index=False, encoding="utf-8")

# -------------------------------------------------------------
# 3. BUILD THE UNIFIED 7-YEAR MASTER EXCEL (2019-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2019_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_meta_2019.to_excel(writer, sheet_name="Audit_Register_2019", index=False)
    df_tax_2019.to_excel(writer, sheet_name="OpenData_2019", index=False)
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

print(f"--> FY 2019 Metadata Audit exported to: {csv_meta_path}")
print(f"--> FY 2019 Master Taxonomy exported to: {csv_tax_path}")
print(f"--> Complete 7-Year Master Excel (2019-2025) generated at: {excel_path}")
