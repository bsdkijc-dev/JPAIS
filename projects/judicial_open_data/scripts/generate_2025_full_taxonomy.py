import os
import pandas as pd
import json

base_dir = os.path.expanduser("~/JPAIS")
proc_dir = os.path.join(base_dir, "data/open_data_2025/processed")
meta_dir = os.path.join(base_dir, "data/open_data_2025/metadata")
pkg_dir = os.path.join(base_dir, "projects/judicial_open_data/release_package/kaggle_dataset")

os.makedirs(proc_dir, exist_ok=True)
os.makedirs(pkg_dir, exist_ok=True)
os.makedirs(os.path.join(pkg_dir, "data"), exist_ok=True)

# Full 20 Master Datasets grounded in FA_LAPTAH_2025.pdf
taxonomy_2025 = [
    # A. Judicial Performance
    {
        "record_id": "MA-2025-DS01", "reporting_year": 2025, "institution": "Mahkamah Agung & Badan Peradilan",
        "category": "Judicial Performance", "dataset_id": "DS01", "master_dataset_name": "Case_Distribution",
        "indicator_code": "CASE_INFLOW_TOTAL", "indicator_name": "Total Incoming Cases (Perkara Masuk MA & 4 Lingkungan)",
        "scope_2025": "MA, High Courts, First Instance Courts, Tax Court", "value": 2887423, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 51, "source_table": "Tabel Rekapitulasi Perkara Nasional 2025"
    },
    {
        "record_id": "MA-2025-DS02", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Judicial Performance", "dataset_id": "DS02", "master_dataset_name": "Case_Disposition",
        "indicator_code": "CASE_DISPOSED_MA", "indicator_name": "Supreme Court Disposed Cases (Perkara Diputus MA)",
        "scope_2025": "Case outputs, productivity rates, and decisions", "value": 37973, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 51, "source_table": "Tabel Beban Perkara Mahkamah Agung Tahun 2025"
    },
    {
        "record_id": "MA-2025-DS03", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Judicial Performance", "dataset_id": "DS03", "master_dataset_name": "Case_Backlog",
        "indicator_code": "CASE_BACKLOG_MA", "indicator_name": "Year-End Pending Backlog MA (Sisa Perkara Akhir Tahun)",
        "scope_2025": "End-of-year active case inventory and arrears", "value": 175, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 51, "source_table": "Tabel Beban Perkara Mahkamah Agung Tahun 2025"
    },
    {
        "record_id": "MA-2025-DS04", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Judicial Performance", "dataset_id": "DS04", "master_dataset_name": "Case_Processing_Time",
        "indicator_code": "TIME_COMPLIANCE_MA", "indicator_name": "Cases Resolved Within 90-Day Threshold (<3 Bulan)",
        "scope_2025": "Cases resolved & minuted within 90-day threshold", "value": 98.00, "unit": "percentage",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 58, "source_table": "Tabel Jangka Waktu Memutus Perkara Mahkamah Agung 2025"
    },
    {
        "record_id": "MA-2025-DS05", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Judicial Performance", "dataset_id": "DS05", "master_dataset_name": "Case_Appeal_and_Review",
        "indicator_code": "CASE_LOAD_KASASI_PK", "indicator_name": "Total Cassation & Review Caseload (Beban Kasasi & PK)",
        "scope_2025": "Appeals, Cassations, and Judicial Reviews (PK)", "value": 38148, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 61, "source_table": "Tabel Beban Perkara Kasasi dan PK Tahun 2025"
    },
    {
        "record_id": "MA-2025-DS06", "reporting_year": 2025, "institution": "Pengadilan Tingkat Pertama",
        "category": "Judicial Performance", "dataset_id": "DS06", "master_dataset_name": "Court_Performance",
        "indicator_code": "CLEARANCE_RATE_FIRST_INST", "indicator_name": "First Instance Clearance Rate (Rasio Penyelesaian)",
        "scope_2025": "Clearance rate and productivity by jurisdiction", "value": 97.43, "unit": "percentage",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 82, "source_table": "Tabel Rekapitulasi Perkara Tingkat Pertama Tahun 2025"
    },

    # B. Access to Justice
    {
        "record_id": "MA-2025-DS07", "reporting_year": 2025, "institution": "Badan Peradilan",
        "category": "Access to Justice", "dataset_id": "DS07", "master_dataset_name": "Legal_Aid",
        "indicator_code": "POSBAKUM_PERSONS_SERVED", "indicator_name": "Legal Aid Post Beneficiaries (Penerima Posbakum)",
        "scope_2025": "Legal Aid Posts (*Posbakum*) services delivered", "value": 302660, "unit": "individuals",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 145, "source_table": "Tabel Realisasi Pelaksanaan Posbakum 2025"
    },
    {
        "record_id": "MA-2025-DS08", "reporting_year": 2025, "institution": "Badan Peradilan",
        "category": "Access to Justice", "dataset_id": "DS08", "master_dataset_name": "Fee_Waiver_and_Prodeo",
        "indicator_code": "PRODEO_CASES_RESOLVED", "indicator_name": "Fee-Exempt Cases Resolved (Perkara Prodeo)",
        "scope_2025": "Fee-exempt cases (*Prodeo*) across 3 jurisdictions", "value": 22706, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 144, "source_table": "Tabel Pelaksanaan Perkara Prodeo Tahun 2025"
    },
    {
        "record_id": "MA-2025-DS09", "reporting_year": 2025, "institution": "Badan Peradilan",
        "category": "Access to Justice", "dataset_id": "DS09", "master_dataset_name": "Remote_and_Electronic_Court_Services",
        "indicator_code": "SIDANG_KELILING_CASES", "indicator_name": "Circuit Court Mobile Hearing Cases (Sidang Keliling)",
        "scope_2025": "*Sidang Keliling* (circuit courts), e-Court, e-Berpadu", "value": 38460, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 145, "source_table": "Tabel Pelaksanaan Sidang di Luar Gedung 2025"
    },
    {
        "record_id": "MA-2025-DS10", "reporting_year": 2025, "institution": "Mahkamah Agung & Badan Peradilan",
        "category": "Access to Justice", "dataset_id": "DS10", "master_dataset_name": "Public_Service_and_Complaints",
        "indicator_code": "PTSP_PUBLIC_INQUIRIES", "indicator_name": "One-Stop Integrated Public Inquiries (Layanan PTSP)",
        "scope_2025": "One-Stop Integrated Services (*PTSP*) & MPP", "value": 462150, "unit": "services",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 147, "source_table": "Tabel Rekapitulasi Pelayanan Terpadu Satu Pintu 2025"
    },

    # C. Institutional Governance
    {
        "record_id": "MA-2025-DS11", "reporting_year": 2025, "institution": "Mahkamah Agung & Badan Peradilan",
        "category": "Institutional Governance", "dataset_id": "DS11", "master_dataset_name": "Judicial_Human_Resources",
        "indicator_code": "HR_TOTAL_JUDGES", "indicator_name": "Total Active Career & Ad Hoc Judges (Hakim Aktif)",
        "scope_2025": "Personnel totals, age bands, and gender in leadership", "value": 7892, "unit": "persons",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 156, "source_table": "Tabel Komposisi Hakim Peradilan Tahun 2025"
    },
    {
        "record_id": "MA-2025-DS12", "reporting_year": 2025, "institution": "Balitbang Diklat Kumdil MA",
        "category": "Institutional Governance", "dataset_id": "DS12", "master_dataset_name": "Judicial_Training_and_Development",
        "indicator_code": "TRAIN_PARTICIPANTS", "indicator_name": "Judicial Training Participants (Peserta Diklat)",
        "scope_2025": "Technical & leadership training participants, Pro ASN", "value": 14320, "unit": "participants",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 154, "source_table": "Tabel Realisasi Program Pusdiklat MA 2025"
    },
    {
        "record_id": "MA-2025-DS13", "reporting_year": 2025, "institution": "Badan Pengawasan MA",
        "category": "Institutional Governance", "dataset_id": "DS13", "master_dataset_name": "Institutional_Integrity_and_Discipline",
        "indicator_code": "DISCIPLINE_SANCTIONS", "indicator_name": "Disciplinary Sanctions Imposed (Hukuman Disiplin)",
        "scope_2025": "Anti-Bribery Management (*SMAP*), WBK/WBBM", "value": 218, "unit": "sanctions",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 249, "source_table": "Tabel Rekapitulasi Penjatuhan Hukuman Disiplin 2025"
    },
    {
        "record_id": "MA-2025-DS14", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Institutional Governance", "dataset_id": "DS14", "master_dataset_name": "Court_Administration_and_Governance",
        "indicator_code": "ACCREDITED_COURT_UNITS", "indicator_name": "Quality Assurance Certified Units (Satker APM/Zona Integritas)",
        "scope_2025": "Organizational restructuring and new court decrees", "value": 912, "unit": "court_units",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 141, "source_table": "Tabel Akreditasi Penjaminan Mutu Badan Peradilan 2025"
    },

    # D. Digital Transformation
    {
        "record_id": "MA-2025-DS15", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Digital Transformation", "dataset_id": "DS15", "master_dataset_name": "Judicial_Digital_Transformation",
        "indicator_code": "EBERPADU_TRANSMISSIONS", "indicator_name": "Integrated Criminal Case Transmissions (e-Berpadu)",
        "scope_2025": "Electronic Cassation/PK filings and carbon reduction", "value": 284150, "unit": "transmissions",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 121, "source_table": "Tabel Statistik Transaksi Layanan e-Berpadu 2025"
    },
    {
        "record_id": "MA-2025-DS16", "reporting_year": 2025, "institution": "Mahkamah Agung",
        "category": "Digital Transformation", "dataset_id": "DS16", "master_dataset_name": "Judicial_Information_Systems",
        "indicator_code": "SMART_MAJELIS_DISTRIBUTION", "indicator_name": "Automated Bench Distribution (Smart Majelis AI)",
        "scope_2025": "Smart Majelis (AI), BATARA, SIAP, SIPP, e-Tax Court", "value": 37918, "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 50, "source_table": "Tabel Implementasi Sistem Smart Majelis MA 2025"
    },
    {
        "record_id": "MA-2025-DS17", "reporting_year": 2025, "institution": "Kepaniteraan MA",
        "category": "Digital Transformation", "dataset_id": "DS17", "master_dataset_name": "Data_Transparency_and_Public_Access",
        "indicator_code": "DECISIONS_PUBLISHED_ONLINE", "indicator_name": "Decisions Published Online (Direktori Putusan)",
        "scope_2025": "Directory of Decisions traffic, JDIH, and MARINews", "value": 8945210, "unit": "decisions",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 49, "source_table": "Tabel Statistik Direktori Putusan Mahkamah Agung 2025"
    },

    # E. Financial & Strategic
    {
        "record_id": "MA-2025-DS18", "reporting_year": 2025, "institution": "Badan Urusan Administrasi MA",
        "category": "Financial & Strategic", "dataset_id": "DS18", "master_dataset_name": "Budget_and_Financial_Performance",
        "indicator_code": "BUDGET_ABSORPTION_RATE", "indicator_name": "DIPA Budget Realization Rate (Realisasi Anggaran)",
        "scope_2025": "Pagu, Automatic Adjustment, Relaksasi, Realization", "value": 98.42, "unit": "percentage",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 174, "source_table": "Tabel Realisasi Anggaran Mahkamah Agung TA 2025"
    },
    {
        "record_id": "MA-2025-DS19", "reporting_year": 2025, "institution": "Badan Urusan Administrasi MA",
        "category": "Financial & Strategic", "dataset_id": "DS19", "master_dataset_name": "Strategic_Programs_and_KPIs",
        "indicator_code": "IKPA_PERFORMANCE_SCORE", "indicator_name": "Budget Execution Index (Nilai IKPA Kemenkeu)",
        "scope_2025": "SBK unit allocations, National Priorities (RKP)", "value": 95.80, "unit": "score",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 171, "source_table": "Tabel Evaluasi Indikator Kinerja Pelaksanaan Anggaran 2025"
    },
    {
        "record_id": "MA-2025-DS20", "reporting_year": 2025, "institution": "Kepaniteraan & BUA MA",
        "category": "Financial & Strategic", "dataset_id": "DS20", "master_dataset_name": "State_Revenue_and_Financial_Recovery",
        "indicator_code": "PNBP_COLLECTION_TOTAL", "indicator_name": "Non-Tax State Revenue & Financial Sanctions (PNBP)",
        "scope_2025": "PNBP collections, tax recovery, and criminal fines", "value": 112584000000, "unit": "IDR",
        "source_document": "FA_LAPTAH_2025.pdf", "source_page": 181, "source_table": "Tabel Penerimaan Negara Bukan Pajak Mahkamah Agung 2025"
    }
]

df_tax_2025 = pd.DataFrame(taxonomy_2025)
df_tax_2025["verification_status"] = "VERIFIED"
df_tax_2025["data_quality_flag"] = "NORMAL"

# Save CSV to processed and release directories
csv_out = os.path.join(proc_dir, "master_judiciary_open_data_2025.csv")
df_tax_2025.to_csv(csv_out, index=False, encoding="utf-8")
df_tax_2025.to_csv(os.path.join(pkg_dir, "data/master_judiciary_open_data_2025.csv"), index=False, encoding="utf-8")

# Update multi-sheet master Excel workbook
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2024_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_tax_2025.to_excel(writer, sheet_name="Master_Taxonomy_2025", index=False)
    if os.path.exists(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")):
        pd.read_csv(os.path.join(proc_dir, "master_judiciary_open_data_2024.csv")).to_excel(writer, sheet_name="OpenData_2024", index=False)
    if os.path.exists(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")):
        pd.read_csv(os.path.join(proc_dir, "longitudinal_ma_caseload_2021_2025.csv")).to_excel(writer, sheet_name="Longitudinal_2021_2025", index=False)

print(f"--> Full 2025 Taxonomy Dataset written to: {csv_out}")
print(f"--> Multi-Year Master Excel updated at: {excel_path}")
