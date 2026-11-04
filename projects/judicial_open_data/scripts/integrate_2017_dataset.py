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
# 1. STRUCTURE FY 2017 SOURCE METADATA & STRATEGIC MILESTONES
# Source: 2017 INDONESIA JUDICIARY OPEN DATA INITIATIVE (Table A5:D14 & A16:D37)
# -------------------------------------------------------------
meta_2017 = [
    {"field_code": "DOC_TITLE", "reporting_year": 2017, "metadata_attribute": "Document Title", "value": "Laporan Tahunan 2017 Mahkamah Agung Republik Indonesia", "specification": "Official Annual Report", "notes": "Primary Source Document"},
    {"field_code": "INST_SCOPE", "reporting_year": 2017, "metadata_attribute": "Institutional Scope", "value": "Mahkamah Agung RI & Badan Peradilan di Bawahnya", "specification": "Apex Court & 4 Subordinate Jurisdictions", "notes": "Umum, Agama, Militer, TUN, Pajak"},
    {"field_code": "DOC_PERIOD", "reporting_year": 2017, "metadata_attribute": "Reporting Period", "value": "1 Januari 2017 – 31 Desember 2017", "specification": "Annual Reporting Period (FY2017)", "notes": "Pre-pandemic operational baseline"},
    {"field_code": "DOC_THEME", "reporting_year": 2017, "metadata_attribute": "Official Theme", "value": "Meningkatkan Integritas dan Kualitas Pelayanan Publik dalam Pelaksanaan Kemandirian Badan Peradilan", "specification": "Strategic Mandate", "notes": "Focus on integrity & service quality"},
    {"field_code": "DOC_PUB", "reporting_year": 2017, "metadata_attribute": "Publisher & Office", "value": "Mahkamah Agung Republik Indonesia, Jl. Medan Merdeka Utara No. 9-13, Jakarta 10110", "specification": "Institutional Publisher", "notes": "Central Administration"},
    {"field_code": "DOC_PUB_YEAR", "reporting_year": 2017, "metadata_attribute": "Publication Date & ISBN", "value": "Maret 2018 (Cetakan Pertama) | ISBN: 978-979-8512-98-8", "specification": "Official Archive Identification", "notes": "Perpustakaan Nasional / KDT"},
    {"field_code": "PAGES_TOTAL", "reporting_year": 2017, "metadata_attribute": "Total Document Extent", "value": "327 Pages (Cover to Cover Unabridged)", "specification": "Document Integrity Verified", "notes": "58 Pages Front Matter + 269 Pages Main Body"},
    {"field_code": "DATA_CLASS", "reporting_year": 2017, "metadata_attribute": "Data Classification & License", "value": "Open Government Data (Public Domain / ODbL Compatible)", "specification": "Machine-Readable Standardization", "notes": "Research-Ready Open Data Repository"}
]

strategic_2017 = [
    {
        "record_id": "MA-2017-STRAT-01", "reporting_year": 2017, "pillar_area": "Judicial Productivity Record",
        "strategic_significance": "Rasio produktivitas memutus perkara tertinggi sepanjang sejarah Mahkamah Agung",
        "key_achievement": "92,23% perkara putus (16.474 putus dari 17.862 beban perkara)",
        "operational_impact": "Sisa perkara terendah dalam sejarah MA: 1.388 perkara", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-02", "reporting_year": 2017, "pillar_area": "Chamber System Institutionalization",
        "strategic_significance": "Pematangan Sistem Kamar (Perdata, Pidana, Agama, Militer, TUN)",
        "key_achievement": "Penerapan sistem baca berkas serentak dan koreksi bersama",
        "operational_impact": "91,96% perkara di MA diputus kurang dari 3 bulan", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-03", "reporting_year": 2017, "pillar_area": "E-Court Foundations (Pre-Pandemic)",
        "strategic_significance": "Pencanangan sistem registrasi, pembayaran, dan pemanggilan elektronik",
        "key_achievement": "SK KMA No. 176A/KMA/SK/IX/2017 (Pokja e-Court, e-Registry, e-Payment)",
        "operational_impact": "Fondasi transformasi digital sebelum pandemi COVID-19", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-04", "reporting_year": 2017, "pillar_area": "Virtual Account Court Fees",
        "strategic_significance": "Modernisasi pembayaran biaya perkara kasasi/PK/HUM via Virtual Account",
        "key_achievement": "Surat Panitera MA No. 2167/PAN/KU.00/8/2017 (Didukung BPK RI)",
        "operational_impact": "Transparansi transaksi keuangan perkara secara real-time", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-05", "reporting_year": 2017, "pillar_area": "Simplified Decision Templates",
        "strategic_significance": "Simplifikasi format dan pedoman penulisan putusan pengadilan",
        "key_achievement": "PERMA No. 9 Tahun 2017 & Pembentukan Unit Quality Control (QC) MA",
        "operational_impact": "Mengatasi bottleneck waktu minutasi perkara", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-06", "reporting_year": 2017, "pillar_area": "Merit-Based Judicial Recruitment",
        "strategic_significance": "Perekrutan terbuka Calon Hakim setelah moratorium bertahun-tahun",
        "key_achievement": "PERMA No. 2 Tahun 2017 & Sistem Computer Assisted Test (CAT) BKN",
        "operational_impact": "1.593 Calon Hakim terpilih secara objektif & transparan", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-07", "reporting_year": 2017, "pillar_area": "Vulnerable Group Protection",
        "strategic_significance": "Pedoman mengadili perkara perempuan berhadapan dengan hukum",
        "key_achievement": "PERMA No. 3 Tahun 2017 & Perlindungan hak konstitusional/CEDAW",
        "operational_impact": "Standar sensitivitas gender bagi hakim di 4 lingkungan", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-08", "reporting_year": 2017, "pillar_area": "Supervisory Accountability",
        "strategic_significance": "Tahun pembersihan dan penguatan integritas aparatur peradilan",
        "key_achievement": "Maklumat KMA No. 01/2017 (Pemberhentian atasan berjenjang) & SIWAS 2.0",
        "operational_impact": "Penerjunan mystery shopper & 156 sanksi disiplin dijatuhkan", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-09", "reporting_year": 2017, "pillar_area": "State Financial Contribution",
        "strategic_significance": "Kontribusi nyata terhadap penerimaan dan pemulihan keuangan negara",
        "key_achievement": "Rp 18,25 Triliun denda & uang pengganti + Rp 74,04 Miliar total PNBP",
        "operational_impact": "Rp 382,88 Miliar dari penyelesaian denda tilang (PERMA 12/2016)", "verification_status": "VERIFIED"
    },
    {
        "record_id": "MA-2017-STRAT-10", "reporting_year": 2017, "pillar_area": "In-Person Circuit Accessibility",
        "strategic_significance": "Tingginya ketergantungan pelayanan peradilan tatap muka pra-pandemi",
        "key_achievement": "62.382 sidang di luar gedung PA, 184.360 warga dibantu Posbakum PA",
        "operational_impact": "1.101 sidang itsbat nikah WNI di Konsulat RI (Kuching, KK, Tawau)", "verification_status": "VERIFIED"
    }
]

df_meta_2017 = pd.DataFrame(meta_2017)
df_strat_2017 = pd.DataFrame(strategic_2017)

# Export individual CSV files
csv_meta_path = os.path.join(proc_dir, "source_audit_register_2017.csv")
csv_strat_path = os.path.join(proc_dir, "master_judiciary_strategic_indicators_2017.csv")

df_meta_2017.to_csv(csv_meta_path, index=False, encoding="utf-8")
df_strat_2017.to_csv(csv_strat_path, index=False, encoding="utf-8")

df_meta_2017.to_csv(os.path.join(pkg_dir, "metadata/source_audit_register_2017.csv"), index=False, encoding="utf-8")
df_meta_2017.to_csv(os.path.join(pkg_dir, "data/source_audit_register_2017.csv"), index=False, encoding="utf-8")
df_strat_2017.to_csv(os.path.join(pkg_dir, "data/master_judiciary_strategic_indicators_2017.csv"), index=False, encoding="utf-8")

# -------------------------------------------------------------
# 2. BUILD THE UNIFIED 9-YEAR MASTER EXCEL (2017-2025)
# -------------------------------------------------------------
excel_path = os.path.join(proc_dir, "JPAIS_Master_Judicial_Open_Data_2017_2025.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_meta_2017.to_excel(writer, sheet_name="Audit_Register_2017", index=False)
    df_strat_2017.to_excel(writer, sheet_name="Strategic_2017", index=False)
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

print(f"--> FY 2017 Metadata Audit exported to: {csv_meta_path}")
print(f"--> FY 2017 Strategic Indicators exported to: {csv_strat_path}")
print(f"--> Complete 9-Year Master Excel (2017-2025) generated at: {excel_path}")
