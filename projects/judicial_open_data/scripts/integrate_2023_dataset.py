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
# 1. STRUCTURE FY 2023 SOURCE AUDIT REGISTER
# Source: 2023 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Sheet: Source_Audit_Register)
# -------------------------------------------------------------
audit_register_2023 = [
    {"register_id": "REG-2023-01", "reporting_year": 2023, "category": "Document Identity", "metadata_property": "Official Document Title", "value_or_reference": "Laporan Tahunan 2023 Mahkamah Agung Republik Indonesia", "source_document": "Laporan Tahunan MA 2023", "page_reference": "Cover & Title Page (pp. 1-2)", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-02", "reporting_year": 2023, "category": "Document Identity", "metadata_property": "Publishing Institution", "value_or_reference": "Mahkamah Agung Republik Indonesia", "source_document": "Laporan Tahunan MA 2023", "page_reference": "Title Page (p. 2)", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-03", "reporting_year": 2023, "category": "Document Identity", "metadata_property": "Reporting Period", "value_or_reference": "1 January 2023 – 31 December 2023 (FY 2023)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "Executive Address (pp. 8-12)", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-04", "reporting_year": 2023, "category": "Document Identity", "metadata_property": "Publication Date & Location", "value_or_reference": "February 2024 / Jakarta, Indonesia", "source_document": "Laporan Tahunan MA 2023", "page_reference": "Sign-off Page (p. 12)", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-05", "reporting_year": 2023, "category": "Document Identity", "metadata_property": "Total Verified Pages", "value_or_reference": "316 Pages", "source_document": "Official PDF Document", "page_reference": "Page Count 1-316", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-06", "reporting_year": 2023, "category": "Document Identity", "metadata_property": "Data Classification & Scope", "value_or_reference": "PUBLIC / Supreme Court & Judicial Bodies", "source_document": "Laporan Tahunan MA 2023", "page_reference": "Overview (pp. 14-16)", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-07", "reporting_year": 2023, "category": "Institutional Scope", "metadata_property": "Jurisdictions Covered", "value_or_reference": "Supreme Court, General, Religious, Military, Administrative, Tax Court", "source_document": "Laporan Tahunan MA 2023", "page_reference": "Table of Contents (pp. 45-51)", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-08", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 1: Case Management (Manajemen Perkara)", "value_or_reference": "Caseload, Productivity, Speed, Minutasi, e-Court, Enforcement", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 53-126", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-09", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 2: Bureaucratic Reform & Access to Justice", "value_or_reference": "WBK/WBBM, Posbakum, Prodeo, Sidang Keliling, Disability Services", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 127-152", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-10", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 3: Judicial Human Resources Management", "value_or_reference": "Composition, Recruitment, Assessment, Diklat, Promotion/Mutation", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 153-168", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-11", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 4: Financial, Asset, and IT Management", "value_or_reference": "DIPA Budget, Realization, BMN Assets, IT Modernization", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 169-198", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-12", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 5: Legal R&D and Landmark Decisions", "value_or_reference": "Legal Research, Landmark Case Rulings across Chambers", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 199-260", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-13", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 6: Judicial Oversight (Pengawasan)", "value_or_reference": "Public Complaints, SMAP, Disciplinary Sanctions, LHKPN", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 261-280", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-14", "reporting_year": 2023, "category": "Reporting Structure", "metadata_property": "Bab 7: Institutional Cooperation", "value_or_reference": "Domestic & International Judicial Collaboration", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 281-308", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-15", "reporting_year": 2023, "category": "Pilot Priority Register", "metadata_property": "Dataset 1: Overall Caseload & Productivity", "value_or_reference": "DS01, DS02, DS03, DS06 (Supreme Court & Jurisdictions)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 66-70, 90, 99", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-16", "reporting_year": 2023, "category": "Pilot Priority Register", "metadata_property": "Dataset 2: Processing Speed & Minutasi", "value_or_reference": "DS03, DS04 (90-Day Benchmark, Minutasi, Backlog)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 70-74, 114-116", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-17", "reporting_year": 2023, "category": "Pilot Priority Register", "metadata_property": "Dataset 3: Access to Justice & Legal Aid", "value_or_reference": "DS07, DS08, DS09, DS10 (Posbakum, Prodeo, e-Court)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 114-116, 146-149", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-18", "reporting_year": 2023, "category": "Pilot Priority Register", "metadata_property": "Dataset 4: Judicial Workforce & Governance", "value_or_reference": "DS11 (Judicial Personnel, Ranks, Positions)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 154-164", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-19", "reporting_year": 2023, "category": "Pilot Priority Register", "metadata_property": "Dataset 5: Financial Execution & State Recovery", "value_or_reference": "DS18, DS20 (Budget Realization, PNBP, Financial Recovery)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "pp. 10, 123-124, 179-181", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-20", "reporting_year": 2023, "category": "Methodology & Schema", "metadata_property": "Standard Metadata Architecture", "value_or_reference": "Multi-dimensional Open Data Schema (22 Standard Fields)", "source_document": "Open Data Initiative Doc", "page_reference": "Section 5", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-21", "reporting_year": 2023, "category": "Methodology & Schema", "metadata_property": "Quality Assurance Protocol", "value_or_reference": "4-Layer Validation: Source, Arithmetic, Cross-Ref, Flagging", "source_document": "Open Data Initiative Doc", "page_reference": "Section 6", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-22", "reporting_year": 2023, "category": "Methodology & Schema", "metadata_property": "Temporal Rule", "value_or_reference": "2023 Primary Observations with 2022 Comparative Baseline", "source_document": "Open Data Initiative Doc", "page_reference": "Sections 1 & 5", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-23", "reporting_year": 2023, "category": "Verification Status", "metadata_property": "Audit Opinion & Integrity", "value_or_reference": "Wajar Tanpa Pengecualian (WTP) 11th Consecutive Year (BPK)", "source_document": "Laporan Tahunan MA 2023", "page_reference": "p. 10, 41, 132", "verification_status": "VERIFIED"},
    {"register_id": "REG-2023-24", "reporting_year": 2023, "category": "Verification Status", "metadata_property": "Data Extraction Engine", "value_or_reference": "Fully Documented Open Data Architecture", "source_document": "Open Data Initiative Doc", "page_reference": "Sections 8-10", "verification_status": "VERIFIED"}
]

df_audit_2023 = pd.DataFrame(audit_register_2023)

# Save to CSV
csv_audit_path = os.path.join(proc_dir, "source_audit_register_2023.csv")
df_audit_2023.to_csv(csv_audit_path, index=False, encoding="utf-8")
df_audit_2023.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2023.csv"), index=False, encoding="utf-8")
df_audit_2023.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2023.csv"), index=False, encoding="utf-8")

# Update Comprehensive Master Excel Workbook (2023-2025)
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2023_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_audit_2023.to_excel(writer, sheet_name="Audit_Register_2023", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")).to_excel(writer, sheet_name="Master_Taxonomy_2025", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")).to_excel(writer, sheet_name="OpenData_2024", index=False)
    if os.path.exists(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")).to_excel(writer, sheet_name="Longitudinal_2021_2025", index=False)

print(f"--> FY 2023 Audit Register exported to: {csv_audit_path}")
print(f"--> Unified Multi-Year Master Excel (2023-2025) generated at: {excel_path}")
