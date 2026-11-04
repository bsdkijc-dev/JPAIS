import os
import pandas as pd

proc_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/processed")
meta_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/metadata")
os.makedirs(proc_dir, exist_ok=True)

# ---------------------------------------------------------
# PILOT 1: DS01 & DS02 - Case Distribution & Disposition (MA & First Instance)
# Source: FA_LAPTAH_2025.pdf, Bab II pp. 51-57 & Bab III pp. 82-114
# ---------------------------------------------------------
caseload_data = [
    {
        "record_id": "REC-2025-CS-001",
        "reporting_year": 2025,
        "institution": "Mahkamah Agung Republik Indonesia",
        "court_level": "Supreme Court (Tingkat Kasasi/PK)",
        "jurisdiction": "All Chambers (Perdata, Pidana, Agama, Militer, TUN)",
        "indicator_code": "PERF_MA_LOAD",
        "indicator_name_id": "Beban Perkara Mahkamah Agung",
        "indicator_name_en": "Supreme Court Caseload Workload",
        "carryover_previous_year": 230,
        "incoming_cases": 37918,
        "total_caseload": 38148,
        "disposed_cases": 37973,
        "withdrawn_cases": 0,
        "remaining_backlog": 175,
        "clearance_rate_pct": 99.54,
        "disposal_target_pct": 90.00,
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 51,
        "source_table": "Tabel Beban Perkara Mahkamah Agung Tahun 2025",
        "data_quality_flag": "VALIDATED",
        "methodological_notes": "Rasio putus 99.54% calculated as Putus / Beban (37,973 / 38,148). Sisa perkara 175 is an all-time low."
    },
    {
        "record_id": "REC-2025-CS-002",
        "reporting_year": 2025,
        "institution": "Pengadilan Tingkat Pertama (4 Lingkungan Peradilan)",
        "court_level": "First Instance Courts",
        "jurisdiction": "Peradilan Umum, Agama, Militer, TUN",
        "indicator_code": "PERF_FIRST_INST_LOAD",
        "indicator_name_id": "Beban Perkara Pengadilan Tingkat Pertama",
        "indicator_name_en": "First Instance Courts Caseload Workload",
        "carryover_previous_year": 73122,
        "incoming_cases": 2849505,
        "total_caseload": 2922627,
        "disposed_cases": 2778855,
        "withdrawn_cases": 68795,
        "remaining_backlog": 74977,
        "clearance_rate_pct": 97.43,
        "disposal_target_pct": 85.00,
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 82,
        "source_table": "Tabel Rekapitulasi Perkara Tingkat Pertama Tahun 2025",
        "data_quality_flag": "VALIDATED",
        "methodological_notes": "Rasio penyelesaian 97.43% calculated as (Putus + Cabut) / Beban. Total beban includes all 4 jurisdictions."
    }
]

# ---------------------------------------------------------
# PILOT 2: DS03 & DS04 - Case Backlog & Processing Time
# Source: FA_LAPTAH_2025.pdf, pp. 58-61
# ---------------------------------------------------------
timeliness_data = [
    {
        "record_id": "REC-2025-TM-001",
        "reporting_year": 2025,
        "institution": "Mahkamah Agung Republik Indonesia",
        "indicator_code": "TIME_MA_DISP_UNDER_3M",
        "indicator_name_id": "Penyelesaian Perkara Kurang dari 3 Bulan",
        "indicator_name_en": "Cases Disposed Within 3 Months",
        "value": 37213,
        "unit": "cases",
        "total_disposed_base": 37973,
        "compliance_pct": 98.00,
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 58,
        "source_table": "Tabel Jangka Waktu Memutus Perkara Mahkamah Agung 2025",
        "data_quality_flag": "VALIDATED",
        "methodological_notes": "Standard SK KMA 214/KMA/SK/XII/2014 sets maximum 90 days deliberation window."
    },
    {
        "record_id": "REC-2025-TM-002",
        "reporting_year": 2025,
        "institution": "Mahkamah Agung Republik Indonesia",
        "indicator_code": "TIME_MA_MINUTASI_UNDER_3M",
        "indicator_name_id": "Minutasi Berkas Putusan Kurang dari 3 Bulan",
        "indicator_name_en": "Case File Minutation & Delivery Under 3 Months",
        "value": 37024,
        "unit": "cases",
        "total_disposed_base": 37973,
        "compliance_pct": 97.50,
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 59,
        "source_table": "Tabel Kinerja Minutasi Perkara 2025",
        "data_quality_flag": "VALIDATED",
        "methodological_notes": "Prompt transmission of official verdict copies to lower courts via electronic delivery."
    }
]

# ---------------------------------------------------------
# PILOT 3: DS07, DS08 & DS09 - Access to Justice Core
# Source: FA_LAPTAH_2025.pdf, pp. 10, 118-123, 144-145
# ---------------------------------------------------------
access_justice_data = [
    {
        "record_id": "REC-2025-A2J-001",
        "reporting_year": 2025,
        "service_name": "Pos Bantuan Hukum (Posbakum)",
        "indicator_code": "A2J_POSBAKUM_PERSONS",
        "indicator_name_id": "Penerima Layanan Posbakum",
        "indicator_name_en": "Legal Aid Post Beneficiaries",
        "value": 302660,
        "unit": "individuals",
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 145,
        "source_table": "Tabel Realisasi Pelaksanaan Posbakum 2025",
        "data_quality_flag": "FLAGGED_DISCREPANCY_NOTED",
        "methodological_notes": "Tabular primary count is 302,660 (p. 145); Executive Summary narrative states 312,358 (p. 10). Tabular value preserved as auditable baseline."
    },
    {
        "record_id": "REC-2025-A2J-002",
        "reporting_year": 2025,
        "service_name": "Perkara Prodeo (Pembebasan Biaya Perkara)",
        "indicator_code": "A2J_PRODEO_CASES",
        "indicator_name_id": "Penyelesaian Perkara Prodeo",
        "indicator_name_en": "Prodeo Fee-Waived Cases Resolved",
        "value": 22706,
        "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 144,
        "source_table": "Tabel Pelaksanaan Perkara Prodeo Tahun 2025",
        "data_quality_flag": "FLAGGED_DISCREPANCY_NOTED",
        "methodological_notes": "Tabular primary count is 22,706 (p. 144); narrative states 22,748 (p. 10). Budget absorption rate achieved 99.1%."
    },
    {
        "record_id": "REC-2025-A2J-003",
        "reporting_year": 2025,
        "service_name": "Sidang di Luar Gedung Pengadilan (Sidang Keliling)",
        "indicator_code": "A2J_CIRCUIT_CASES",
        "indicator_name_id": "Penyelesaian Perkara Sidang Keliling",
        "indicator_name_en": "Circuit Court Mobile Hearing Cases Resolved",
        "value": 38460,
        "unit": "cases",
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 145,
        "source_table": "Tabel Pelaksanaan Sidang di Luar Gedung 2025",
        "data_quality_flag": "FLAGGED_DISCREPANCY_NOTED",
        "methodological_notes": "Tabular primary count is 38,460 (p. 145); narrative summary states 40,057 (p. 10). Primarily marriage validation and civil registration in remote regions."
    },
    {
        "record_id": "REC-2025-A2J-004",
        "reporting_year": 2025,
        "service_name": "Layanan Pengadilan Elektronik (e-Court)",
        "indicator_code": "A2J_ECOURT_TOTAL_USERS",
        "indicator_name_id": "Pengguna Layanan e-Court Terdaftar",
        "indicator_name_en": "Registered e-Court Users (Advocate & Non-Advocate)",
        "value": 395120,
        "unit": "registered_users",
        "source_document": "FA_LAPTAH_2025.pdf",
        "source_page": 118,
        "source_table": "Tabel Pengguna Layanan e-Court Tahun 2025",
        "data_quality_flag": "VALIDATED",
        "methodological_notes": "Includes 67,412 registered advocates and 327,708 individual/corporate verified litigants."
    }
]

df_caseload = pd.DataFrame(caseload_data)
df_timeliness = pd.DataFrame(timeliness_data)
df_access = pd.DataFrame(access_justice_data)

# Export individual CSVs
df_caseload.to_csv(os.path.join(proc_dir, "pilot_caseload_disposition.csv"), index=False, encoding="utf-8")
df_timeliness.to_csv(os.path.join(proc_dir, "pilot_timeliness_backlog.csv"), index=False, encoding="utf-8")
df_access.to_csv(os.path.join(proc_dir, "pilot_access_to_justice.csv"), index=False, encoding="utf-8")

# Export consolidated Excel Workbook
wb_path = os.path.join(proc_dir, "JPAIS_Pilot_Judicial_Open_Data_2025.xlsx")
with pd.ExcelWriter(wb_path, engine="openpyxl") as writer:
    df_caseload.to_excel(writer, sheet_name="Caseload_Disposition", index=False)
    df_timeliness.to_excel(writer, sheet_name="Timeliness_Backlog", index=False)
    df_access.to_excel(writer, sheet_name="Access_to_Justice", index=False)

print(f"Pilot datasets successfully extracted to CSVs in: {proc_dir}")
print(f"Master Excel workbook generated at: {wb_path}")
