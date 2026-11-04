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
# 1. FY 2020 SOURCE AUDIT & RECONCILIATION DATASET
# -------------------------------------------------------------
audit_2020 = [
    {"record_id": "MA-2020-META-01", "reporting_year": 2020, "category": "Document Identity", "field_name": "Document Title", "value": "Laporan Tahunan 2020 Mahkamah Agung Republik Indonesia", "citation": "Cover & Title Page (hal. 1-3)", "status": "VERIFIED"},
    {"record_id": "MA-2020-META-02", "reporting_year": 2020, "category": "Document Identity", "field_name": "Publication Theme", "value": "Optimalisasi Peradilan Modern Berkelanjutan, Merespons Pandemik Covid-19", "citation": "Laptah 2020 hal. 1, 12", "status": "VERIFIED"},
    {"record_id": "MA-2020-META-03", "reporting_year": 2020, "category": "Document Identity", "field_name": "Publisher / Institution", "value": "Mahkamah Agung Republik Indonesia", "citation": "Laptah 2020 hal. 1, 16", "status": "VERIFIED"},
    {"record_id": "MA-2020-META-04", "reporting_year": 2020, "category": "Document Identity", "field_name": "Total Volume / Pages", "value": "362 Halaman", "citation": "Laptah 2020 PDF Metadata (hal. 1-362)", "status": "VERIFIED"},
    {"record_id": "MA-2020-META-05", "reporting_year": 2020, "category": "Document Identity", "field_name": "Chief Justice (Ketua MA RI)", "value": "Dr. H. Muhammad Syarifuddin, S.H., M.H.", "citation": "Laptah 2020 hal. 5, 21, 39", "status": "VERIFIED"},
    {"record_id": "MA-2020-META-06", "reporting_year": 2020, "category": "Document Identity", "field_name": "Preceding Chief Justice", "value": "Prof. Dr. M. Hatta Ali, S.H., M.H.", "citation": "Laptah 2020 hal. 5, 23, 39", "status": "VERIFIED"},
    {"record_id": "MA-2020-RECON-01", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "MA Workload Balance", "value": "20.761", "citation": "Workload = Sisa 2019 + Masuk 2020 (hal. 91)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-02", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "MA Ending Backlog Balance", "value": "199", "citation": "Ending = Workload - Putus - Cabut (hal. 91)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-03", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "National Workload Balance", "value": "3.955.963", "citation": "National Workload = Sisa 2019 + Masuk (hal. 91)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-04", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "National Ending Backlog", "value": "85.807", "citation": "Ending = Workload - Putus - Cabut (hal. 91)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-05", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "MA Deciding Productivity Rate", "value": "99,04%", "citation": "Productivity = Putus / Workload (hal. 91, 95)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-06", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "Budget Realization Rate", "value": "95,28%", "citation": "Realization = Realisasi / Pagu DIPA (hal. 14, 233)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-07", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "Total Potensi Keuangan Negara", "value": "Rp 58.507.022.411.536", "citation": "Total Denda + Uang Pengganti Pidana (hal. 124, 155)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-08", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "On-Time Case Processing Rate", "value": "96,65%", "citation": "On-Time = Putus < 3 Bulan / Total Putus (hal. 65, 96)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-09", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "e-Court YoY Growth Rate", "value": "295,79%", "citation": "Growth = (2020 - 2019) / 2019 (hal. 147)", "status": "PERFECT RECONCILIATION"},
    {"record_id": "MA-2020-RECON-10", "reporting_year": 2020, "category": "Arithmetic Reconciliation", "field_name": "Total Hakim Korps Nasional", "value": "8.439", "citation": "Total Hakim = MA + Banding + Pertama (hal. 154, 195)", "status": "PERFECT RECONCILIATION"}
]

# -------------------------------------------------------------
# 2. FY 2020 20 MASTER DATASET TAXONOMY (DS01 - DS20)
# -------------------------------------------------------------
taxonomy_2020 = [
    {"record_id": "MA-2020-DS01", "reporting_year": 2020, "dataset_id": "DS01", "category": "Judicial Performance", "master_dataset_name": "Case_Distribution", "indicator": "Incoming Cases (Perkara Masuk)", "lineage": "Bab I (hal. 91, 93, 94, 100-149)"},
    {"record_id": "MA-2020-DS02", "reporting_year": 2020, "dataset_id": "DS02", "category": "Judicial Performance", "master_dataset_name": "Case_Disposition", "indicator": "Disposed Cases (Perkara Diputus)", "lineage": "Bab I (hal. 91, 97, 98, 100-149)"},
    {"record_id": "MA-2020-DS03", "reporting_year": 2020, "dataset_id": "DS03", "category": "Judicial Performance", "master_dataset_name": "Case_Backlog", "indicator": "Ending Backlog 199 (MA) / 85,807 (National)", "lineage": "Bab I (hal. 64, 91, 95, 97)"},
    {"record_id": "MA-2020-DS04", "reporting_year": 2020, "dataset_id": "DS04", "category": "Judicial Performance", "master_dataset_name": "Case_Processing_Time", "indicator": "Resolution within 90 Days (< 3 Bulan): 96.65%", "lineage": "Bab I (hal. 65, 96, 97, 99)"},
    {"record_id": "MA-2020-DS05", "reporting_year": 2020, "dataset_id": "DS05", "category": "Judicial Performance", "master_dataset_name": "Case_Appeal_and_Review", "indicator": "Appeals (Banding), Cassation, Judicial Review (PK)", "lineage": "Bab I (hal. 94, 98, 120, 150-151)"},
    {"record_id": "MA-2020-DS06", "reporting_year": 2020, "dataset_id": "DS06", "category": "Judicial Performance", "master_dataset_name": "Court_Performance", "indicator": "MA Productivity 99.04%; Clearance Rate Benchmark", "lineage": "Bab I (hal. 91, 95, 98, 150-155)"},
    {"record_id": "MA-2020-DS07", "reporting_year": 2020, "dataset_id": "DS07", "category": "Access to Justice", "master_dataset_name": "Legal_Aid", "indicator": "Pos Bantuan Hukum (Posbakum) Consultations", "lineage": "Bab II (hal. 161, 180)"},
    {"record_id": "MA-2020-DS08", "reporting_year": 2020, "dataset_id": "DS08", "category": "Access to Justice", "master_dataset_name": "Fee_Waiver_and_Prodeo", "indicator": "Prodeo Fee-Waived Cases across Jurisdictions", "lineage": "Bab II (hal. 161, 180)"},
    {"record_id": "MA-2020-DS09", "reporting_year": 2020, "dataset_id": "DS09", "category": "Access to Justice", "master_dataset_name": "Remote_and_Electronic_Court_Services", "indicator": "115,455 Remote Trials; 8,560 e-Litigation Hearings", "lineage": "Bab I (hal. 147-149), Bab II (hal. 160, 174)"},
    {"record_id": "MA-2020-DS10", "reporting_year": 2020, "dataset_id": "DS10", "category": "Access to Justice", "master_dataset_name": "Public_Service_and_Complaints", "indicator": "Circuit Courts (Sidang Keliling) & PTSP Desks", "lineage": "Bab II (hal. 161, 180), Bab VI (hal. 303, 322)"},
    {"record_id": "MA-2020-DS11", "reporting_year": 2020, "dataset_id": "DS11", "category": "Institutional Governance", "master_dataset_name": "Judicial_Human_Resources", "indicator": "8,439 Judges; 30,551 Total Judicial Workforce", "lineage": "Bab I (hal. 154-155), Bab III (hal. 195)"},
    {"record_id": "MA-2020-DS12", "reporting_year": 2020, "dataset_id": "DS12", "category": "Institutional Governance", "master_dataset_name": "Judicial_Training_and_Development", "indicator": "Online Judicial Training (MURI Record 16,963)", "lineage": "hal. 14, 44, Bab III (hal. 199-210)"},
    {"record_id": "MA-2020-DS13", "reporting_year": 2020, "dataset_id": "DS13", "category": "Institutional Governance", "master_dataset_name": "Institutional_Integrity_and_Discipline", "indicator": "SMAP Anti-Bribery; 94 WBK/WBBM Integrity Units", "lineage": "hal. 13, 160, Bab VI (hal. 304, 310-318)"},
    {"record_id": "MA-2020-DS14", "reporting_year": 2020, "dataset_id": "DS14", "category": "Institutional Governance", "master_dataset_name": "Court_Administration_and_Governance", "indicator": "Quality Accreditation (APM) & SIPERMARI Asset App", "lineage": "Bab I (hal. 81-90), Bab II (hal. 160, 177)"},
    {"record_id": "MA-2020-DS15", "reporting_year": 2020, "dataset_id": "DS15", "category": "Digital Transformation", "master_dataset_name": "Judicial_Digital_Transformation", "indicator": "e-Court v3 Upaya Hukum Banding & Digital Folders", "lineage": "Bab I (hal. 76, 83-86), Bab IV (hal. 256)"},
    {"record_id": "MA-2020-DS16", "reporting_year": 2020, "dataset_id": "DS16", "category": "Digital Transformation", "master_dataset_name": "Judicial_Information_Systems", "indicator": "SIPP, SIAP-MA, SIWAS, PMPZI Centralization", "lineage": "Bab I (hal. 82-89), Bab VI (hal. 300, 322)"},
    {"record_id": "MA-2020-DS17", "reporting_year": 2020, "dataset_id": "DS17", "category": "Digital Transformation", "master_dataset_name": "Data_Transparency_and_Public_Access", "indicator": "Direktori Putusan v3 (5.65M total / 1.17M in 2020)", "lineage": "hal. 14, 65, 87-88, 182, 268"},
    {"record_id": "MA-2020-DS18", "reporting_year": 2020, "dataset_id": "DS18", "category": "Financial & Strategic", "master_dataset_name": "Budget_and_Financial_Performance", "indicator": "Pagu Rp9.855T; Realisasi Rp9.390T (95.28%); WTP ke-8", "lineage": "hal. 14, 47, Bab IV (hal. 233-242)"},
    {"record_id": "MA-2020-DS19", "reporting_year": 2020, "dataset_id": "DS19", "category": "Financial & Strategic", "master_dataset_name": "Strategic_Programs_and_KPIs", "indicator": "Cetaktak Biru 2010-2035 2nd Phase Completion", "lineage": "hal. 66-70, 85-88"},
    {"record_id": "MA-2020-DS20", "reporting_year": 2020, "dataset_id": "DS20", "category": "Financial & Strategic", "master_dataset_name": "State_Revenue_and_Financial_Recovery", "indicator": "PNBP Rp71.71B; Potential Recovery Rp58.51T", "lineage": "Bab I (hal. 155-156), Bab IV (hal. 242)"}
]

df_audit_2020 = pd.DataFrame(audit_2020)
df_tax_2020 = pd.DataFrame(taxonomy_2020)

# Export individual CSVs
csv_audit_path = os.path.join(proc_dir, "source_audit_register_2020.csv")
csv_tax_path = os.path.join(proc_dir, "master_judiciary_open_data_2020.csv")

df_audit_2020.to_csv(csv_audit_path, index=False, encoding="utf-8")
df_tax_2020.to_csv(csv_tax_path, index=False, encoding="utf-8")

df_audit_2020.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2020.csv"), index=False, encoding="utf-8")
df_audit_2020.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2020.csv"), index=False, encoding="utf-8")
df_tax_2020.to_csv(os.path.join(pkg_dir, "data/master_judiciary_open_data_2020.csv"), index=False, encoding="utf-8")

# -------------------------------------------------------------
# 3. BUILD THE COMPREHENSIVE 6-YEAR MASTER EXCEL (2020-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2020_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_audit_2020.to_excel(writer, sheet_name="Audit_Register_2020", index=False)
    df_tax_2020.to_excel(writer, sheet_name="OpenData_2020", index=False)
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

print(f"--> FY 2020 Source Audit exported to: {csv_audit_path}")
print(f"--> FY 2020 Master Taxonomy exported to: {csv_tax_path}")
print(f"--> Comprehensive 6-Year Master Excel (2020-2025) generated at: {excel_path}")
