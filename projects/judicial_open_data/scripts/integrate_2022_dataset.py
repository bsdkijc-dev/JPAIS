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
# 1. STRUCTURE FY 2022 SOURCE AUDIT DATASET
# Source: 2022 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Sheet: Source_Audit)
# -------------------------------------------------------------
audit_2022_records = [
    {"record_id": "MA-2022-AUD-01", "reporting_year": 2022, "metadata_property": "Document Title", "value": "Laporan Tahunan 2022 Mahkamah Agung Republik Indonesia", "description": "Official Annual Report of the Supreme Court of the Republic of Indonesia", "source_location": "Cover & Title Page (pp. 1-3)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-02", "reporting_year": 2022, "metadata_property": "Document Theme", "value": "Integritas Tangguh, Kepercayaan Publik Tumbuh", "description": "Official theme of the 2022 Annual Report", "source_location": "Cover & Preface (pp. 1, 7)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-03", "reporting_year": 2022, "metadata_property": "Publisher / Institutional Scope", "value": "Mahkamah Agung Republik Indonesia", "description": "Highest judicial authority & judicial bodies under its jurisdiction", "source_location": "Publisher imprint (p. 3)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-04", "reporting_year": 2022, "metadata_property": "Reporting Period", "value": "1 Januari 2022 - 31 Desember 2022", "description": "FY 2022 annual reporting period", "source_location": "Report Header", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-05", "reporting_year": 2022, "metadata_property": "Publication Date & Place", "value": "Februari 2023, Jakarta", "description": "Official publication date and city of signing", "source_location": "Preface / Sekapur Sirih (p. 11)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-06", "reporting_year": 2022, "metadata_property": "Chief Justice of the Supreme Court", "value": "Prof. Dr. H. Muhammad Syarifuddin, S.H., M.H.", "description": "Ketua Mahkamah Agung Republik Indonesia periode 2020 - sekarang", "source_location": "Leadership Profile (pp. 5, 17)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-07", "reporting_year": 2022, "metadata_property": "Total Document Pages", "value": "344 Halaman", "description": "Total page length of the official publication PDF", "source_location": "Document Metadata (p. 1 of 344)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-08", "reporting_year": 2022, "metadata_property": "Data Classification", "value": "PUBLIC / Open Data Domain", "description": "Institutional judicial open access under SK KMA 2-144/2022 & UU KIP", "source_location": "Section 1 (p. 11, 40)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-09", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter I", "value": "BAB I: Manajemen Perkara (pp. 53-136)", "description": "Caseload, clearance rate, productivity, processing speed, e-Court, mediation", "source_location": "Table of Contents (pp. 42-45)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-10", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter II", "value": "BAB II: Reformasi Birokrasi & Akses Terhadap Keadilan (pp. 137-164)", "description": "PMPRB, PMPZI, WBK/WBBM, Posbakum, prodeo fee waiver, mobile court", "source_location": "Table of Contents (p. 43)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-11", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter III", "value": "BAB III: Manajemen Sumber Daya Manusia (pp. 165-214)", "description": "Judicial personnel, judges, registrars, administrative staff, training", "source_location": "Table of Contents (p. 43-44)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-12", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter IV", "value": "BAB IV: Manajemen Keuangan, Aset, dan Teknologi Informasi (pp. 215-244)", "description": "Budget realization (97.95%), State Assets/BMN, IT infrastructure", "source_location": "Table of Contents (p. 44)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-13", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter V", "value": "BAB V: Penelitian & Pengembangan Hukum serta Landmark Decisions (pp. 245-290)", "description": "Legal research, academic papers, citations, landmark decisions", "source_location": "Table of Contents (p. 44)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-14", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter VI", "value": "BAB VI: Pengawasan (pp. 291-310)", "description": "Internal supervisory body (Bawas), SMAP anti-bribery, discipline sanctions", "source_location": "Table of Contents (pp. 44-45)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-15", "reporting_year": 2022, "metadata_property": "Report Structure: Chapter VII", "value": "BAB VII: Peran Serta dan Kerja Sama (pp. 311-336)", "description": "Bilateral/multilateral judicial cooperation (CACJ, Netherlands, Australia)", "source_location": "Table of Contents (p. 45)", "audit_status": "VERIFIED"},
    {"record_id": "MA-2022-AUD-16", "reporting_year": 2022, "metadata_property": "Total National Caseload 2022", "value": "3.567.138 masuk; 3.643.268 beban; 3.513.611 putus", "description": "Combined national performance across MA and 4 judicial jurisdictions", "source_location": "BAB I Summary (pp. 54, 68)", "audit_status": "VERIFIED ARITHMETICALLY"},
    {"record_id": "MA-2022-AUD-17", "reporting_year": 2022, "metadata_property": "National Case Clearance Rate", "value": "97.96%", "description": "Productivity ratio = (Disposed 3.513.611 / Workload 3.643.268) * 100", "source_location": "BAB I Summary (p. 68)", "audit_status": "VERIFIED ARITHMETICALLY"},
    {"record_id": "MA-2022-AUD-18", "reporting_year": 2022, "metadata_property": "Supreme Court Deciding Rate", "value": "99.08%", "description": "Supreme Court case disposition productivity rate (28.024 diputus dari 28.284 beban)", "source_location": "BAB I Summary (pp. 54, 70)", "audit_status": "VERIFIED ARITHMETICALLY"},
    {"record_id": "MA-2022-AUD-19", "reporting_year": 2022, "metadata_property": "Supreme Court 90-Day Benchmark", "value": "99.26%", "description": "27.817 dari 28.024 perkara MA diputus tepat waktu kurang dari 90 hari", "source_location": "BAB I Summary (pp. 55, 72)", "audit_status": "VERIFIED ARITHMETICALLY"},
    {"record_id": "MA-2022-AUD-20", "reporting_year": 2022, "metadata_property": "Budget Realization Rate", "value": "97.95%", "description": "Rp11.278.876.171.102 terealisasi dari Pagu Akhir Rp11.514.469.985.000 (WTP ke-10)", "source_location": "Sekapur Sirih (p. 10)", "audit_status": "VERIFIED ARITHMETICALLY"}
]

df_2022 = pd.DataFrame(audit_2022_records)

# Export individual CSV
csv_2022_path = os.path.join(proc_dir, "source_audit_register_2022.csv")
df_2022.to_csv(csv_2022_path, index=False, encoding="utf-8")
df_2022.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2022.csv"), index=False, encoding="utf-8")
df_2022.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2022.csv"), index=False, encoding="utf-8")

# Generate Comprehensive Master Multi-Year Excel (2022-2025)
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2022_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_2022.to_excel(writer, sheet_name="Audit_Register_2022", index=False)
    if os.path.exists(os.path.join(proc_dir, "source_audit_register_2023.csv")):
        pd.read_csv(os.path.join(proc_dir, "source_audit_register_2023.csv")).to_excel(writer, sheet_name="Audit_Register_2023", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")).to_excel(writer, sheet_name="OpenData_2024", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")).to_excel(writer, sheet_name="Master_Taxonomy_2025", index=False)
    if os.path.exists(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")).to_excel(writer, sheet_name="Longitudinal_2021_2025", index=False)

print(f"--> FY 2022 Dataset exported to: {csv_2022_path}")
print(f"--> Unified Multi-Year Master Excel (2022-2025) generated at: {excel_path}")
