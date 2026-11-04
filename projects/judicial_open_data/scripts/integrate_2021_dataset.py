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
# 1. JURISDICTION CASELOAD PERFORMANCE 2021
# -------------------------------------------------------------
caseload_2021 = [
    {
        "record_id": "MA-2021-CASE-01", "reporting_year": 2021, "jurisdiction_level": "Mahkamah Agung (Supreme Court)",
        "court_type": "Apex Court", "previous_backlog_2020": 199, "incoming_filings_2021": 19209,
        "total_workload": 19408, "decisions_rendered": 19233, "withdrawn_cases": 0, "ending_backlog_2021": 175,
        "clearance_productivity_ratio_pct": 99.10, "source_document": "Laporan Tahunan 2021 Mahkamah Agung RI",
        "source_page": 58, "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2021-CASE-02", "reporting_year": 2021, "jurisdiction_level": "Pengadilan Tingkat Banding (Appellate)",
        "court_type": "High Courts (4 Jurisdictions)", "previous_backlog_2020": 2580, "incoming_filings_2021": 23688,
        "total_workload": 26268, "decisions_rendered": 23772, "withdrawn_cases": 29, "ending_backlog_2021": 2467,
        "clearance_productivity_ratio_pct": 90.50, "source_document": "Laporan Tahunan 2021 Mahkamah Agung RI",
        "source_page": 60, "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2021-CASE-03", "reporting_year": 2021, "jurisdiction_level": "Pengadilan Tingkat Pertama (First Instance)",
        "court_type": "General, Religious, Military, Administrative", "previous_backlog_2020": 75598, "incoming_filings_2021": 2691649,
        "total_workload": 2767247, "decisions_rendered": 2652790, "withdrawn_cases": 53147, "ending_backlog_2021": 61310,
        "clearance_productivity_ratio_pct": 97.78, "source_document": "Laporan Tahunan 2021 Mahkamah Agung RI",
        "source_page": 62, "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2021-CASE-04", "reporting_year": 2021, "jurisdiction_level": "Pengadilan Pajak (Tax Court)",
        "court_type": "Tax Court (Specialized)", "previous_backlog_2020": 7430, "incoming_filings_2021": 17654,
        "total_workload": 25084, "decisions_rendered": 12906, "withdrawn_cases": 0, "ending_backlog_2021": 12178,
        "clearance_productivity_ratio_pct": 51.45, "source_document": "Laporan Tahunan 2021 Mahkamah Agung RI",
        "source_page": 64, "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2021-CASE-05", "reporting_year": 2021, "jurisdiction_level": "Total Nasional (National Aggregate)",
        "court_type": "All Jurisdictions Combined", "previous_backlog_2020": 85807, "incoming_filings_2021": 2752200,
        "total_workload": 2838007, "decisions_rendered": 2708701, "withdrawn_cases": 53176, "ending_backlog_2021": 76130,
        "clearance_productivity_ratio_pct": 97.32, "source_document": "Laporan Tahunan 2021 Mahkamah Agung RI",
        "source_page": 54, "verification_status": "VERIFIED ARITHMETICALLY"
    }
]

# -------------------------------------------------------------
# 2. KEY STRATEGIC & ACCESS TO JUSTICE INDICATORS 2021
# -------------------------------------------------------------
strategic_2021 = [
    {"record_id": "MA-2021-STRAT-01", "reporting_year": 2021, "thematic_domain": "Access to Justice", "indicator_name": "Pos Bantuan Hukum (Posbakum) Services", "value": 114311, "unit": "Service Hours", "context": "Free legal aid consultations across General, Religious, and TUN courts (p. 145)"},
    {"record_id": "MA-2021-STRAT-02", "reporting_year": 2021, "thematic_domain": "Access to Justice", "indicator_name": "Fee-Exempt Litigation (Prodeo)", "value": 3333, "unit": "Cases", "context": "Full fee waivers for underprivileged litigants across 3 jurisdictions (p. 144)"},
    {"record_id": "MA-2021-STRAT-03", "reporting_year": 2021, "thematic_domain": "Access to Justice", "indicator_name": "Circuit Courts (Sidang di Luar Gedung)", "value": 10461, "unit": "Hearings", "context": "Remote hearings overcoming geographical barriers + 184 integrated services (p. 145)"},
    {"record_id": "MA-2021-STRAT-04", "reporting_year": 2021, "thematic_domain": "Digital Transformation", "indicator_name": "e-Court First-Instance Case Filings", "value": 225072, "unit": "Cases", "context": "20.37% YoY expansion (PN 90,041; PA 132,869; PTUN 2,162) (p. 115)"},
    {"record_id": "MA-2021-STRAT-05", "reporting_year": 2021, "thematic_domain": "Digital Transformation", "indicator_name": "Criminal Teleconference Hearings", "value": 129575, "unit": "Cases", "context": "Remote hearing safety protocol during COVID-19 pandemic (p. 116)"},
    {"record_id": "MA-2021-STRAT-06", "reporting_year": 2021, "thematic_domain": "Digital Transformation", "indicator_name": "Public Decisions Directory Uploads", "value": 980654, "unit": "Decisions", "context": "Court decisions published online for public transparency (p. 148)"},
    {"record_id": "MA-2021-STRAT-07", "reporting_year": 2021, "thematic_domain": "Human Resources", "indicator_name": "Total Judicial Institutional Workforce", "value": 30551, "unit": "Personnel", "context": "Across 917 units: 8,323 judges, 11,734 registry staff, 9,342 admin (p. 154)"},
    {"record_id": "MA-2021-STRAT-08", "reporting_year": 2021, "thematic_domain": "Fiscal Performance", "indicator_name": "Total Realized Budget Expenditure", "value": 10509269716263, "unit": "IDR", "context": "97.96% realization of revised Pagu; 9th consecutive WTP audit opinion (p. 12)"},
    {"record_id": "MA-2021-STRAT-09", "reporting_year": 2021, "thematic_domain": "State Financial Recovery", "indicator_name": "Total Potential Financial Recovery", "value": 73900163398681, "unit": "IDR", "context": "Aggregate potential revenue from criminal fines and restitution (p. 124)"}
]

df_caseload_2021 = pd.DataFrame(caseload_2021)
df_strat_2021 = pd.DataFrame(strategic_2021)

# Export individual CSV files
csv_case_path = os.path.join(proc_dir, "master_judiciary_caseload_2021.csv")
csv_strat_path = os.path.join(proc_dir, "master_judiciary_strategic_indicators_2021.csv")

df_caseload_2021.to_csv(csv_case_path, index=False, encoding="utf-8")
df_strat_2021.to_csv(csv_strat_path, index=False, encoding="utf-8")

df_caseload_2021.to_csv(os.path.join(pkg_dir, "data/master_judiciary_caseload_2021.csv"), index=False, encoding="utf-8")
df_strat_2021.to_csv(os.path.join(pkg_dir, "data/master_judiciary_strategic_indicators_2021.csv"), index=False, encoding="utf-8")

# -------------------------------------------------------------
# 3. BUILD THE UNIFIED 5-YEAR MASTER WORKBOOK (2021-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2021_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_caseload_2021.to_excel(writer, sheet_name="Caseload_2021", index=False)
    df_strat_2021.to_excel(writer, sheet_name="Strategic_2021", index=False)
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

print(f"--> FY 2021 Caseload Dataset exported to: {csv_case_path}")
print(f"--> FY 2021 Strategic Dataset exported to: {csv_strat_path}")
print(f"--> Complete 5-Year Master Excel (2021-2025) generated at: {excel_path}")
