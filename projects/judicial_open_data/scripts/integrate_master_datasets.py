import os
import pandas as pd

proc_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/processed")
meta_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/metadata")
os.makedirs(proc_dir, exist_ok=True)
os.makedirs(meta_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. LONGITUDINAL TREND DATASET (2021-2025): Supreme Court Performance
# Source: FA_LAPTAH_2025.pdf, Bab II p. 53 (Tabel Tren Perkara MA 2021-2025)
# ---------------------------------------------------------
longitudinal_ma_data = [
    {"reporting_year": 2021, "carryover_previous_year": 192, "incoming_cases": 19208, "total_caseload": 19400, "disposed_cases": 19233, "remaining_backlog": 167, "clearance_rate_pct": 99.14},
    {"reporting_year": 2022, "carryover_previous_year": 167, "incoming_cases": 28284, "total_caseload": 28451, "disposed_cases": 28024, "remaining_backlog": 427, "clearance_rate_pct": 98.50},
    {"reporting_year": 2023, "carryover_previous_year": 427, "incoming_cases": 27252, "total_caseload": 27679, "disposed_cases": 27512, "remaining_backlog": 167, "clearance_rate_pct": 99.40},
    {"reporting_year": 2024, "carryover_previous_year": 167, "incoming_cases": 30514, "total_caseload": 30681, "disposed_cases": 30451, "remaining_backlog": 230, "clearance_rate_pct": 99.25},
    {"reporting_year": 2025, "carryover_previous_year": 230, "incoming_cases": 37918, "total_caseload": 38148, "disposed_cases": 37973, "remaining_backlog": 175, "clearance_rate_pct": 99.54}
]
df_longitudinal = pd.DataFrame(longitudinal_ma_data)
df_longitudinal["institution"] = "Mahkamah Agung Republik Indonesia"
df_longitudinal["source_document"] = "FA_LAPTAH_2025.pdf"
df_longitudinal["source_page"] = 53
df_longitudinal["source_table"] = "Tabel Perkembangan Perkara Mahkamah Agung 2021-2025"

# ---------------------------------------------------------
# 2. MASTER 20 DATASETS SUMMARY REGISTRY (FY 2025 Comprehensive)
# Sources: FA_LAPTAH_2025.pdf across Chapters I-VII
# ---------------------------------------------------------
master_indicators = [
    # A. Judicial Performance
    {"dataset_id": "DS01", "category": "Judicial Performance", "code": "CASE_DIST", "name_id": "Distribusi Perkara Masuk MA", "name_en": "Supreme Court Case Intake Distribution", "value": 37918, "unit": "cases", "page": 51},
    {"dataset_id": "DS02", "category": "Judicial Performance", "code": "CASE_DISP", "name_id": "Penyelesaian Perkara MA", "name_en": "Supreme Court Case Disposition", "value": 37973, "unit": "cases", "page": 51},
    {"dataset_id": "DS03", "category": "Judicial Performance", "code": "CASE_BACKLOG", "name_id": "Sisa Perkara Akhir Tahun MA", "name_en": "Year-End Supreme Court Backlog", "value": 175, "unit": "cases", "page": 51},
    {"dataset_id": "DS04", "category": "Judicial Performance", "code": "CASE_TIME", "name_id": "Penyelesaian Tepat Waktu (<3 Bulan)", "name_en": "Timely Case Resolution (<3 Months)", "value": 98.00, "unit": "percent", "page": 58},
    {"dataset_id": "DS05", "category": "Judicial Performance", "code": "CASE_APPEAL", "name_id": "Beban Perkara Kasasi & Peninjauan Kembali", "name_en": "Cassation & Judicial Review Caseload", "value": 38148, "unit": "cases", "page": 61},
    {"dataset_id": "DS06", "category": "Judicial Performance", "code": "COURT_PERF", "name_id": "Penyelesaian Perkara Tingkat Pertama", "name_en": "First Instance Disposition Volume", "value": 2778855, "unit": "cases", "page": 82},
    
    # B. Access to Justice
    {"dataset_id": "DS07", "category": "Access to Justice", "code": "A2J_POSBAKUM", "name_id": "Penerima Layanan Posbakum", "name_en": "Legal Aid Post Beneficiaries", "value": 302660, "unit": "individuals", "page": 145},
    {"dataset_id": "DS08", "category": "Access to Justice", "code": "A2J_PRODEO", "name_id": "Perkara Prodeo (Pembebasan Biaya)", "name_en": "Prodeo Fee-Waived Cases Resolved", "value": 22706, "unit": "cases", "page": 144},
    {"dataset_id": "DS09", "category": "Access to Justice", "code": "A2J_REMOTE", "name_id": "Perkara Sidang di Luar Gedung", "name_en": "Circuit Court Mobile Hearing Cases", "value": 38460, "unit": "cases", "page": 145},
    {"dataset_id": "DS10", "category": "Access to Justice", "code": "A2J_COMPLAINT", "name_id": "Pengaduan Masyarakat via SIWAS", "name_en": "Public Whistleblowing Complaints (SIWAS)", "value": 4125, "unit": "complaints", "page": 246},
    
    # C. Institutional Governance
    {"dataset_id": "DS11", "category": "Institutional Governance", "code": "GOV_HR", "name_id": "Jumlah Hakim Seluruh Indonesia", "name_en": "Total Active Judges (All Jurisdictions)", "value": 7892, "unit": "judges", "page": 156},
    {"dataset_id": "DS12", "category": "Institutional Governance", "code": "GOV_TRAIN", "name_id": "Peserta Pelatihan Pusdiklat MA", "name_en": "Judicial Training Academy Participants", "value": 14320, "unit": "participants", "page": 154},
    {"dataset_id": "DS13", "category": "Institutional Governance", "code": "GOV_DISCIPLINE", "name_id": "Penjatuhan Hukuman Disiplin", "name_en": "Disciplinary Sanctions Imposed", "value": 218, "unit": "personnel", "page": 249},
    {"dataset_id": "DS14", "category": "Institutional Governance", "code": "GOV_ADMIN", "name_id": "Satuan Kerja Terakreditasi Penjaminan Mutu", "name_en": "Quality Assurance Accredited Court Units", "value": 912, "unit": "court_units", "page": 141},
    
    # D. Digital Transformation
    {"dataset_id": "DS15", "category": "Digital Transformation", "code": "DIG_TRANS", "name_id": "Pelimpahan Berkas Pidana Terpadu (e-Berpadu)", "name_en": "Integrated Criminal Case Files (e-Berpadu)", "value": 284150, "unit": "transmissions", "page": 121},
    {"dataset_id": "DS16", "category": "Digital Transformation", "code": "DIG_SYSTEMS", "name_id": "Distribusi Perkara Otomatis (Smart Majelis)", "name_en": "Automated Bench Distribution (Smart Majelis)", "value": 37918, "unit": "cases", "page": 50},
    {"dataset_id": "DS17", "category": "Digital Transformation", "code": "DIG_ACCESS", "name_id": "Putusan Terunggah di Direktori Putusan", "name_en": "Court Decisions Published Online", "value": 8945210, "unit": "decisions", "page": 49},
    
    # E. Financial & Strategic Accountability
    {"dataset_id": "DS18", "category": "Financial & Strategic", "code": "FIN_BUDGET", "name_id": "Realisasi Anggaran Mahkamah Agung (DIPA)", "name_en": "Budget Execution Absorption Rate", "value": 98.42, "unit": "percent", "page": 174},
    {"dataset_id": "DS19", "category": "Financial & Strategic", "code": "FIN_KPI", "name_id": "Indikator Kinerja Pelaksanaan Anggaran (IKPA)", "name_en": "Budget Execution Performance Index (IKPA)", "value": 95.80, "unit": "score", "page": 171},
    {"dataset_id": "DS20", "category": "Financial & Strategic", "code": "FIN_RECOVERY", "name_id": "Penerimaan Negara Bukan Pajak (PNBP)", "name_en": "Non-Tax State Revenue Collected", "value": 112584000000, "unit": "IDR", "page": 181}
]
df_master = pd.DataFrame(master_indicators)
df_master["reporting_year"] = 2025
df_master["institution"] = "Mahkamah Agung Republik Indonesia"
df_master["source_document"] = "FA_LAPTAH_2025.pdf"

# ---------------------------------------------------------
# 3. DATA DICTIONARY & INDICATOR METHODOLOGY
# ---------------------------------------------------------
data_dict = [
    {"field_name": "record_id", "data_type": "string", "description": "Unique identifier for each data observation"},
    {"field_name": "reporting_year", "data_type": "integer", "description": "Calendar fiscal reporting year (e.g. 2025)"},
    {"field_name": "institution", "data_type": "string", "description": "Reporting judicial authority or jurisdiction"},
    {"field_name": "category", "data_type": "string", "description": "Functional taxonomy pillar (A through E)"},
    {"field_name": "indicator_code", "data_type": "string", "description": "Standardized machine-readable indicator token"},
    {"field_name": "indicator_name_id", "data_type": "string", "description": "Official Indonesian title per Mahkamah Agung annual report"},
    {"field_name": "indicator_name_en", "data_type": "string", "description": "Standardized English translation of the indicator"},
    {"field_name": "value", "data_type": "float/integer", "description": "Reported quantitative metric value"},
    {"field_name": "unit", "data_type": "string", "description": "Measurement unit (cases, percent, individuals, IDR, etc.)"},
    {"field_name": "source_document", "data_type": "string", "description": "Official file name of the primary publication"},
    {"field_name": "source_page", "data_type": "integer", "description": "Page number in official PDF source"},
    {"field_name": "data_quality_flag", "data_type": "string", "description": "Validation status (VALIDATED, FLAGGED_DISCREPANCY_NOTED)"}
]
df_dict = pd.DataFrame(data_dict)

# Export CSV artifacts
df_longitudinal.to_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv"), index=False, encoding="utf-8")
df_master.to_csv(os.path.join(proc_dir, "master_20_indicators_2025.csv"), index=False, encoding="utf-8")
df_dict.to_csv(os.path.join(meta_dir, "data_dictionary.csv"), index=False, encoding="utf-8")

# Update Master Excel Workbook with full master sheets
wb_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2025.xlsx")
with pd.ExcelWriter(wb_path, engine="openpyxl") as writer:
    df_master.to_excel(writer, sheet_name="Master_20_Indicators", index=False)
    df_longitudinal.to_excel(writer, sheet_name="Longitudinal_2021_2025", index=False)
    df_dict.to_excel(writer, sheet_name="Data_Dictionary", index=False)

print(f"Master longitudinal dataset exported to: {proc_dir}/longitudinal_ma_caseload_2021_2025.csv")
print(f"Master 20 indicators exported to: {proc_dir}/master_20_indicators_2025.csv")
print(f"Data Dictionary exported to: {meta_dir}/data_dictionary.csv")
print(f"Master consolidated workbook generated at: {wb_path}")
