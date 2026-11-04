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
# 1. STRUCTURE FY 2018 SOURCE AUDIT REGISTER
# Source: 2018 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A4:F32)
# -------------------------------------------------------------
audit_2018 = [
    # Document Identity
    {"record_id": "MA-2018-DOC-01", "reporting_year": 2018, "section": "Document Identity", "attribute": "Document Title", "parameter_value": "Laporan Tahunan 2018 Mahkamah Agung Republik Indonesia", "source_specification": "Official Printed / PDF Publication", "verification_status": "VERIFIED", "notes": "Published by Mahkamah Agung RI"},
    {"record_id": "MA-2018-DOC-02", "reporting_year": 2018, "section": "Document Identity", "attribute": "Institutional Scope", "parameter_value": "Mahkamah Agung RI and Subordinate Courts", "source_specification": "Apex Court + 4 Jurisdictions + Tax Court", "verification_status": "VERIFIED", "notes": "Covers all judicial branches across 34 provinces"},
    {"record_id": "MA-2018-DOC-03", "reporting_year": 2018, "section": "Document Identity", "attribute": "Reporting Year", "parameter_value": "2018", "source_specification": "Calendar & Fiscal Year (Jan 1 - Dec 31, 2018)", "verification_status": "VERIFIED", "notes": "Temporal baseline: Pre-pandemic reporting year"},
    {"record_id": "MA-2018-DOC-04", "reporting_year": 2018, "section": "Document Identity", "attribute": "Publication Date", "parameter_value": "Februari 2019", "source_specification": "Jakarta, Indonesia; ISBN: 978-979-8512-99-5", "verification_status": "VERIFIED", "notes": "Official editorial board release"},
    {"record_id": "MA-2018-DOC-05", "reporting_year": 2018, "section": "Document Identity", "attribute": "Document Volume", "parameter_value": "316 Pages", "source_specification": "Complete Digital Master Copy", "verification_status": "VERIFIED", "notes": "Includes statistical tables, infographics, narrative"},
    {"record_id": "MA-2018-DOC-06", "reporting_year": 2018, "section": "Document Identity", "attribute": "Primary Theme", "parameter_value": "Era Baru Peradilan Modern Berbasis Teknologi Informasi", "source_specification": "Official Cover Title & Focus", "verification_status": "VERIFIED", "notes": "Milestone launch of PERMA No. 3/2018 & e-Court"},
    {"record_id": "MA-2018-DOC-07", "reporting_year": 2018, "section": "Document Identity", "attribute": "Data Classification", "parameter_value": "PUBLIC OPEN DATA", "source_specification": "Official Unrestricted Release", "verification_status": "VERIFIED", "notes": "Open data ingestion for research and policy"},
    {"record_id": "MA-2018-DOC-08", "reporting_year": 2018, "section": "Document Identity", "attribute": "Comparative Baseline", "parameter_value": "FY 2017", "source_specification": "Only where officially reported in 2018 publication", "verification_status": "VERIFIED", "notes": "Preserves historical temporal integrity"},

    # Report Structure & Chapter Boundaries
    {"record_id": "MA-2018-CHAP-01", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Prelim: Foreword & Institutional Profile", "parameter_value": "Sekapur Sirih & Tentang Mahkamah Agung", "source_specification": "pp. 14–56", "verification_status": "VERIFIED", "notes": "Court leadership, mission, organizational structure, milestones"},
    {"record_id": "MA-2018-CHAP-02", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab I: Judicial Case Management", "parameter_value": "Manajemen Perkara", "source_specification": "pp. 57–128", "verification_status": "VERIFIED", "notes": "Caseload, incoming, disposed, backlog, turnaround, minutasi, PNBP"},
    {"record_id": "MA-2018-CHAP-03", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab II: Bureaucratic Reform & Access to Justice", "parameter_value": "Reformasi Birokrasi dan Akses Terhadap Keadilan", "source_specification": "pp. 129–152", "verification_status": "VERIFIED", "notes": "e-Court, Posbakum legal aid, prodeo fee waivers, circuit courts, APM"},
    {"record_id": "MA-2018-CHAP-04", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab III: Judicial Human Resources", "parameter_value": "Manajemen Sumber Daya Manusia", "source_specification": "pp. 153–174", "verification_status": "VERIFIED", "notes": "Staffing bezetting, judges, clerks, open recruitment, training"},
    {"record_id": "MA-2018-CHAP-05", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab IV: Financial, Asset & IT Management", "parameter_value": "Manajemen Keuangan, Aset, dan TIK", "source_specification": "pp. 175–206", "verification_status": "VERIFIED", "notes": "Budget execution, PNBP revenues, state assets (BMN), IT governance"},
    {"record_id": "MA-2018-CHAP-06", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab V: Judicial Research & Precedents", "parameter_value": "Litbang Kumdil dan Landmark Decisions", "source_specification": "pp. 207–234", "verification_status": "VERIFIED", "notes": "Legal research, downloads, milestone judicial precedents"},
    {"record_id": "MA-2018-CHAP-07", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab VI: Judicial Oversight & Ethics", "parameter_value": "Pengawasan", "source_specification": "pp. 235–254", "verification_status": "VERIFIED", "notes": "Public complaints, SIWAS whistleblowing, MKH disciplinary actions"},
    {"record_id": "MA-2018-CHAP-08", "reporting_year": 2018, "section": "Chapter Inventory", "attribute": "Bab VII: National & International Relations", "parameter_value": "Peran Serta Mahkamah Agung", "source_specification": "pp. 255–278", "verification_status": "VERIFIED", "notes": "Bilateral judicial cooperation, donor programs, legal diplomacy"},

    # Priority Dataset Extraction Mapping
    {"record_id": "MA-2018-PILOT-01", "reporting_year": 2018, "section": "Priority Dataset", "attribute": "DS01: Overall Caseload & Productivity", "parameter_value": "DS01_Caseload_Productivity", "source_specification": "Tabel pp. 72–73, 80", "verification_status": "VERIFIED ARITHMETICALLY", "notes": "Sisa 2017, Masuk 2018, Beban, Putus, Cabut, Sisa 2018, Rasio Putus"},
    {"record_id": "MA-2018-PILOT-02", "reporting_year": 2018, "section": "Priority Dataset", "attribute": "DS04: Case Processing Speed & Minutasi", "parameter_value": "DS04_Processing_Speed", "source_specification": "Tabel pp. 76–78, 83–84", "verification_status": "VERIFIED ARITHMETICALLY", "notes": "Disposition <3 Mos, Minutasi Duration, Clearance Rate, Active Inventory"},
    {"record_id": "MA-2018-PILOT-03", "reporting_year": 2018, "section": "Priority Dataset", "attribute": "DS07: Access to Justice & Legal Aid", "parameter_value": "DS07_Access_to_Justice", "source_specification": "Tabel pp. 138–144, 183", "verification_status": "VERIFIED", "notes": "Posbakum, Prodeo, Sidang Luar Gedung, e-Court Implementation"},
    {"record_id": "MA-2018-PILOT-04", "reporting_year": 2018, "section": "Priority Dataset", "attribute": "DS11: Judicial Workforce & Human Resources", "parameter_value": "DS11_Judicial_Workforce", "source_specification": "Tabel pp. 158–161, 123", "verification_status": "VERIFIED", "notes": "Total Personnel, Judge/Clerk Bezetting, Judge-to-Case Workload Ratios"},
    {"record_id": "MA-2018-PILOT-05", "reporting_year": 2018, "section": "Priority Dataset", "attribute": "DS18: Budget Performance & Revenue Recovery", "parameter_value": "DS18_Financial_Execution", "source_specification": "Tabel pp. 188–190, 125", "verification_status": "VERIFIED ARITHMETICALLY", "notes": "Budget Allocation, Realization %, PNBP Accounts, Fine/Restitution Recoveries"}
]

df_audit_2018 = pd.DataFrame(audit_2018)

# Export individual CSV files
csv_2018_path = os.path.join(proc_dir, "source_audit_register_2018.csv")
df_audit_2018.to_csv(csv_2018_path, index=False, encoding="utf-8")
df_audit_2018.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2018.csv"), index=False, encoding="utf-8")
df_audit_2018.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2018.csv"), index=False, encoding="utf-8")

# -------------------------------------------------------------
# 2. BUILD THE UNIFIED 8-YEAR MASTER EXCEL (2018-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2018_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_audit_2018.to_excel(writer, sheet_name="Audit_Register_2018", index=False)
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

print(f"--> FY 2018 Source Audit Register exported to: {csv_2018_path}")
print(f"--> Complete 8-Year Master Excel (2018-2025) generated at: {excel_path}")
