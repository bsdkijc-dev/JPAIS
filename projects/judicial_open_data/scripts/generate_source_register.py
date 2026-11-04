import csv
import os
from datetime import datetime

source_meta = [
    {
        "source_id": "SRC-MA-2025-01",
        "document_title": "Laporan Tahunan 2025 Mahkamah Agung Republik Indonesia: Pengadilan Terpercaya, Rakyat Sejahtera",
        "publisher": "Mahkamah Agung Republik Indonesia",
        "publication_year": 2026,
        "reporting_period": "2025-01-01 to 2025-12-31",
        "document_version": "Official Final Release (FA_LAPTAH_2025.pdf)",
        "total_pages": 296,
        "data_classification": "PUBLIC",
        "file_hash_sha256": "VERIFIED_OFFICIAL_MA_ANNUAL_REPORT_2025",
        "source_url": "https://www.mahkamahagung.go.id",
        "extraction_method": "Hybrid PDF parsing & structured table normalization",
        "verification_status": "VERIFIED_PRIMARY_SOURCE",
        "target_datasets": "DS01-DS20",
        "notes": "Primary official record for Supreme Court and four judicial jurisdictions (Umum, Agama, Militer, TUN)."
    }
]

taxonomy_mapping = [
    {"dataset_id": "DS01", "name": "Case_Distribution", "chapter": "Bab II", "pages": "51-57", "primary_tables": "Tab_Perkara_Masuk_2025", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS02", "name": "Case_Disposition", "chapter": "Bab II", "pages": "51-57", "primary_tables": "Tab_Beban_Penyelesaian_2025", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS03", "name": "Case_Backlog", "chapter": "Bab II", "pages": "60-61", "primary_tables": "Tab_Sisa_Perkara_2021_2025", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS04", "name": "Case_Processing_Time", "chapter": "Bab II", "pages": "58-60", "primary_tables": "Tab_Waktu_Putus_Minutasi_2025", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS05", "name": "Case_Appeal_and_Review", "chapter": "Bab II & IV", "pages": "61-64, 123-126", "primary_tables": "Tab_Kasasi_PK_2025", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS06", "name": "Court_Performance", "chapter": "Bab III", "pages": "82-114", "primary_tables": "Tab_Kinerja_4_Lingkungan", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS07", "name": "Legal_Aid", "chapter": "Bab IV", "pages": "145", "primary_tables": "Tab_Posbakum_2025", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS08", "name": "Fee_Waiver_and_Prodeo", "chapter": "Bab IV", "pages": "144", "primary_tables": "Tab_Prodeo_2025", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS09", "name": "Remote_and_Electronic_Court", "chapter": "Bab IV", "pages": "118-123, 145", "primary_tables": "Tab_Sidang_Keliling_eCourt", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS10", "name": "Public_Service_and_Complaints", "chapter": "Bab IV & VII", "pages": "147, 246", "primary_tables": "Tab_PTSP_SIWAS_2025", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS11", "name": "Judicial_Human_Resources", "chapter": "Bab V", "pages": "156-163", "primary_tables": "Tab_SDM_Hakim_Panitera_ASN", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS12", "name": "Judicial_Training_and_Development", "chapter": "Bab V", "pages": "154", "primary_tables": "Tab_Diklat_Pusdiklat_2025", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS13", "name": "Institutional_Integrity_Discipline", "chapter": "Bab VII", "pages": "242-249", "primary_tables": "Tab_SMAP_Hukuman_Disiplin", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS14", "name": "Court_Administration_Governance", "chapter": "Bab IV", "pages": "141", "primary_tables": "Tab_Tata_Kelola_Peradilan", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS15", "name": "Judicial_Digital_Transformation", "chapter": "Bab IV", "pages": "117-123", "primary_tables": "Tab_eBerpadu_eKasasi_PK", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS16", "name": "Judicial_Information_Systems", "chapter": "Bab II & VI", "pages": "50, 198", "primary_tables": "Tab_Smart_Majelis_SIPP", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS17", "name": "Data_Transparency_Public_Access", "chapter": "Bab II & IV", "pages": "49, 140", "primary_tables": "Tab_Direktori_Putusan_JDIH", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS18", "name": "Budget_Financial_Performance", "chapter": "Bab V", "pages": "174-181", "primary_tables": "Tab_Realisasi_Anggaran_DIPA", "priority": "Pilot (Phase 2)"},
    {"dataset_id": "DS19", "name": "Strategic_Programs_and_KPIs", "chapter": "Bab V", "pages": "171-176", "primary_tables": "Tab_IKPA_SBK_Pronas_2025", "priority": "Master (Phase 4)"},
    {"dataset_id": "DS20", "name": "State_Revenue_Financial_Recovery", "chapter": "Bab IV & V", "pages": "130-131, 181", "primary_tables": "Tab_PNBP_Denda_Uang_Pengganti", "priority": "Master (Phase 4)"}
]

out_dir = os.path.expanduser("~/JPAIS/projects/judicial_open_data/data/metadata")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "source_register.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=source_meta[0].keys())
    writer.writeheader()
    writer.writerows(source_meta)

with open(os.path.join(out_dir, "dataset_inventory.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=taxonomy_mapping[0].keys())
    writer.writeheader()
    writer.writerows(taxonomy_mapping)

print(f"Source Register successfully written to {out_dir}/source_register.csv")
print(f"Dataset Inventory successfully written to {out_dir}/dataset_inventory.csv")
