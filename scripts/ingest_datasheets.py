import csv
import os

os.makedirs("datasets/verified", exist_ok=True)

# 1. Export Statutory Terms from Data Sheet
terms = [
    {"Istilah Hukum": "Hakim", "Definisi": "Hakim agung dan hakim pada peradilan di bawahnya", "Dasar Hukum": "Pasal 4 ayat (1) dan (2) UU No. 5 Tahun 2004", "Status": "Eksplisit"},
    {"Istilah Hukum": "Majelis hakim", "Definisi": "Susunan hakim yang memeriksa dan memutus perkara", "Dasar Hukum": "Pasal 40 ayat (1) UU No. 14 Tahun 1985", "Status": "Implisit"},
    {"Istilah Hukum": "Musyawarah majelis", "Definisi": "Rapat rahasia untuk mengambil keputusan", "Dasar Hukum": "Pasal 30 ayat (2) dan (3) UU No. 5 Tahun 2004", "Status": "Doktrinal"},
    {"Istilah Hukum": "Dissenting opinion", "Definisi": "Pendapat berbeda dari putusan mayoritas", "Dasar Hukum": "Pasal 30 ayat (3) UU No. 5 Tahun 2004", "Status": "Doktrinal"},
    {"Istilah Hukum": "Concurring opinion", "Definisi": "Alasan berbeda dari putusan mayoritas", "Dasar Hukum": "Pasal 30 ayat (2) UU No. 5 Tahun 2004", "Status": "Doktrinal"}
]

with open("datasets/verified/istilah_hukum.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Istilah Hukum", "Definisi", "Dasar Hukum", "Status"])
    writer.writeheader()
    writer.writerows(terms)

# 2. Export Court Decisions from Data Sheets
cases = [
    {"case_number": "17 PK/Pdt.Sus-Pailit/2020", "applicant": "PT Atakana Company", "court": "Mahkamah Agung", "verdict": "Ditolak", "reason": "Novum tidak menentukan under Art 295(2)(a)"},
    {"case_number": "02/Pdt.Sus-Pailit/2019/PN Niaga Jkt.Pst", "applicant": "PT Nurtransmandiri", "court": "PN Niaga Jakarta Pusat", "verdict": "Ditolak", "reason": "Gagal melampirkan laporan keuangan/neraca audit"},
    {"case_number": "12/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst", "applicant": "PT Jaya Pacific Propertindo", "court": "PN Niaga Jakarta Pusat", "verdict": "Ditolak", "reason": "Ketiadaan bukti utang asli dan klausul force majeure tidak sederhana"},
    {"case_number": "18/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst", "applicant": "Siti Nurjanah", "court": "PN Niaga Jakarta Pusat", "verdict": "Ditolak", "reason": "Legal standing kreditur WNA diragukan"},
    {"case_number": "28/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst", "applicant": "PT Persada Nusantara Steel", "court": "PN Niaga Jakarta Pusat", "verdict": "Ditolak", "reason": "Gagal membuktikan keberadaan dua atau lebih kreditur"},
    {"case_number": "420/Pdt.Sus-PKPU/2021/PN.Niaga.Jkt.Pst", "applicant": "PT Bata Mera Wisesa", "court": "PN Niaga Jakarta Pusat", "verdict": "Homologasi", "reason": "Perdamaian disahkan"},
    {"case_number": "70/Pdt.Sus-PKPU/2020/PN.Niaga.Jkt.Pst", "applicant": "PT Anantara Resources", "court": "PN Niaga Jakarta Pusat", "verdict": "PKPU Sementara", "reason": "PKPU Sementara dikabulkan 45 hari"},
    {"case_number": "245/Pdt.Sus-PKPU/2020/PN.Niaga.Jkt.Pst", "applicant": "PT Pohon Besar Perkasa", "court": "PN Niaga Jakarta Pusat", "verdict": "Pailit", "reason": "Debitor tidak mengajukan rencana perdamaian"}
]

with open("datasets/verified/indonesian_court_cases.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["case_number", "applicant", "court", "verdict", "reason"])
    writer.writeheader()
    writer.writerows(cases)

print("Ingestion files successfully created in ~/JPAIS/datasets/verified/")
