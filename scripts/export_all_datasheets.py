import csv
import os

target_dir = os.path.expanduser("~/JPAIS/datasets/verified")
os.makedirs(target_dir, exist_ok=True)

# 1. Analisis Istilah Hukum
t1 = [
    {"Istilah": "Hakim", "Definisi": "Hakim agung dan hakim pada peradilan di bawahnya", "Dasar_Hukum": "Pasal 4 ayat (1) dan (2) UU No. 5 Tahun 2004", "Status": "Tegas / Eksplisit tertulis"},
    {"Istilah": "Majelis hakim", "Definisi": "Susunan hakim yang memeriksa dan memutus perkara", "Dasar_Hukum": "Pasal 40 ayat (1) UU No. 14 Tahun 1985", "Status": "Implisit"},
    {"Istilah": "Musyawarah majelis", "Definisi": "Rapat rahasia untuk mengambil keputusan", "Dasar_Hukum": "Pasal 30 ayat (2) & (3) UU 5/2004; Pasal 40 ayat (2) UU 14/1985", "Status": "Doktrinal dan praktik peradilan"},
    {"Istilah": "Pertimbangan hukum tertulis", "Definisi": "Pendapat tertulis hakim anggota", "Dasar_Hukum": "Pasal 30 ayat (2) UU No. 5 Tahun 2004", "Status": "Konsisten kewajiban eksplisit"},
    {"Istilah": "Dissenting opinion", "Definisi": "Pendapat berbeda dari putusan mayoritas", "Dasar_Hukum": "Pasal 30 ayat (3) UU No. 5 Tahun 2004", "Status": "Doktrinal dan praktik peradilan"},
    {"Istilah": "Concurring opinion", "Definisi": "Alasan berbeda dari putusan mayoritas (sependapat amar)", "Dasar_Hukum": "Pasal 30 ayat (2) UU No. 5 Tahun 2004", "Status": "Doktrinal dan praktik peradilan"}
]
with open(f"{target_dir}/analisis_istilah_hukum.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t1[0].keys()); w.writeheader(); w.writerows(t1)

# 2. Risiko Pelanggaran Kerahasiaan Musyawarah
t2 = [
    {"Bentuk_Risiko": "Bocornya isi permusyawaratan sebelum diucapkan", "Konsekuensi": "Mengganggu sahnya proses pengambilan putusan & menurunkan kepercayaan publik", "Dasar_Hukum": "Pasal 14 ayat (1) & (2) UU 48/2009", "Ketentuan_Sanksi": "Pelanggaran langsung rahasia permusyawaratan hakim"},
    {"Bentuk_Risiko": "Intervensi eksternal setelah bocoran", "Konsekuensi": "Menggerus kemandirian hakim yang wajib dijaga", "Dasar_Hukum": "Pasal 3 ayat (1), (2), (3) UU 48/2009", "Ketentuan_Sanksi": "Sanksi pidana campur tangan peradilan & etik hakim"},
    {"Bentuk_Risiko": "Tekanan dan relasi kuasa internal berbasis sikap dini", "Konsekuensi": "Menciptakan chilling effect pada hakim berbeda pendapat", "Dasar_Hukum": "Pasal 39 ayat (4) UU 48/2009; Pasal 13D UU 49/2009", "Ketentuan_Sanksi": "Pelanggaran Kode Etik dan Pedoman Perilaku Hakim (KEPPH)"},
    {"Bentuk_Risiko": "Pengungkapan individual vote di luar kerangka dissent", "Konsekuensi": "Merusak prinsip kolegialitas dan memicu ancaman personal", "Dasar_Hukum": "Pasal 14 ayat (3) UU 48/2009; Pasal 25 ayat (5) UU 2/1986", "Ketentuan_Sanksi": "Pelanggaran KEPPH objek pengawasan Komisi Yudisial"},
    {"Bentuk_Risiko": "Penyalahgunaan informasi untuk insider dealing", "Konsekuensi": "Jual-beli bocoran putusan dan kerugian pihak berperkara", "Dasar_Hukum": "Pasal 20 ayat (1) UU 49/2009; Pasal 11A UU 5/2004", "Ketentuan_Sanksi": "Pemberhentian tidak dengan hormat via Majelis Kehormatan Hakim (MKH)"}
]
with open(f"{target_dir}/risiko_kerahasiaan_musyawarah.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t2[0].keys()); w.writeheader(); w.writerows(t2)

# 3. Dasar Hukum Persidangan Elektronik MA
t3 = [
    {"Ketentuan": "Legalitas umum musyawarah elektronik/hibrid", "Regulasi": "PERMA 1/2019 jo. PERMA 7/2022", "Dimensi": "Yuridis & SPBE", "Keamanan": "Memenuhi standar perlindungan data sistem elektronik"},
    {"Ketentuan": "Pengucapan dan verifikasi putusan pidana", "Regulasi": "PERMA 4/2020 jo. PERMA 8/2022", "Dimensi": "Duty of Care & Sakralitas", "Keamanan": "Verifikasi berlapis digital dan naskah manual"},
    {"Ketentuan": "Upaya hukum banding, kasasi, dan PK via SIP", "Regulasi": "PERMA 4/2020 jo. PERMA 8/2022", "Dimensi": "Efisiensi Peradilan", "Keamanan": "Prosedur verifikasi berkas bundel elektronik"},
    {"Ketentuan": "Keabsahan informasi elektronik sebagai bukti sah", "Regulasi": "UU ITE Pasal 5 ayat (1)-(3)", "Dimensi": "Legalitas Pembuktian", "Keamanan": "Sistem elektronik andal dan tersertifikasi"},
    {"Ketentuan": "Tanggung jawab Penyelenggara Sistem Elektronik", "Regulasi": "PP 71/2019 Pasal 26; Perpres 95/2018", "Dimensi": "SPBE Nasional", "Keamanan": "Kontrol keamanan berlapis pada semua fase administrasi"},
    {"Ketentuan": "Rekam jejak audit dan masa retensi dokumen", "Regulasi": "PP 71/2019 Pasal 22, 24, 25", "Dimensi": "Audit Trail & Keamanan", "Keamanan": "Audit logging ketat, tamper-proof, dan backup retensi"}
]
with open(f"{target_dir}/persidangan_elektronik_ma.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t3[0].keys()); w.writeheader(); w.writerows(t3)

# 4. Mekanisme Deliberasi Hakim
t4 = [
    {"Aspek": "Pertimbangan Tertulis Ex-Ante", "Dasar_Hukum": "Pasal 2 ayat (1), Pasal 14 ayat (2) UU 48/2009", "Tujuan": "Pre-commitment rasional sebelum terpapar tekanan kolegial", "Dampak": "Menghilangkan sikap ikut ketua, memperkuat otonomi nurani"},
    {"Aspek": "Junior-First Voting", "Dasar_Hukum": "Pasal 14 ayat (1), Pasal 14 ayat (2) UU 48/2009", "Tujuan": "Memutus bias jangkar (anchoring) dan bias otoritas senior", "Dampak": "Ruang deliberasi steril dari dominasi feodalisme senioritas"},
    {"Aspek": "Keterikatan Personal Alasan Putusan", "Dasar_Hukum": "Pasal 50 ayat (1), Pasal 53 ayat (2) UU 48/2009", "Tujuan": "Akuntabilitas penalaran hukum (ratio decidendi)", "Dampak": "Pertanggungjawaban koherensi argumentasi personal hakim"},
    {"Aspek": "Pencegahan Free-Rider Judge", "Dasar_Hukum": "Pasal 5 ayat (2)-(3), Pasal 39 ayat (3) UU 48/2009", "Tujuan": "Mencegah hakim menumpang kerja analitis rekan sejawat", "Dampak": "Kualitas analisis teruji sejak awal dalam forum rapat tertutup"}
]
with open(f"{target_dir}/mekanisme_musyawarah_deliberasi.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t4[0].keys()); w.writeheader(); w.writerows(t4)

# 5. Prinsip Pengambilan Keputusan Majelis
t5 = [
    {"Dimensi": "Filosofis", "Prinsip": "Keutamaan Mufakat Kolegial", "Dasar_Hukum": "Pasal 2 ayat (1), Pasal 14 ayat (1) UU 48/2009", "Prosedur": "Deliberasi mendalam nurani bersama", "Tujuan": "Ekspresi amanat transenden Ketuhanan YME"},
    {"Dimensi": "Filosofis", "Prinsip": "Favor Reo / In Dubio Pro Reo", "Dasar_Hukum": "Asas Hukum Pidana (KUHAP)", "Prosedur": "Bila deadlock suara seimbang, pilih yang menguntungkan terdakwa", "Tujuan": "Perlindungan martabat dan ultima ratio pidana"},
    {"Dimensi": "Filosofis", "Prinsip": "Favor Contractus", "Dasar_Hukum": "Pasal 1343-1347 KUHPerdata", "Prosedur": "Penafsiran yang mempertahankan keberlakuan kontrak", "Tujuan": "Kepastian stabilitas transaksi perdata"},
    {"Dimensi": "Yuridis", "Prinsip": "Voting Safety Valve & Dissenting", "Dasar_Hukum": "Pasal 14 ayat (3) UU 48/2009", "Prosedur": "Voting prosedural jika mufakat gagal dan catat dissent", "Tujuan": "Kepastian putusan final tanpa menutupi pluralitas hakim"}
]
with open(f"{target_dir}/prinsip_pengambilan_keputusan.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t5[0].keys()); w.writeheader(); w.writerows(t5)

# 6. Pengelolaan Arsip Musyawarah
t6 = [
    {"Regulasi": "UU 43/2009", "Pasal": "Pasal 33, 34", "Klasifikasi": "Arsip Negara / Sangat Rahasia", "Substansi": "Draf dan risalah musyawarah wajib dilindungi dari sabotase"},
    {"Regulasi": "UU 48/2009", "Pasal": "Pasal 14 ayat (1)-(4)", "Klasifikasi": "Rahasia Jabatan / Tertutup Mutlak", "Substansi": "Substansi musyawarah mutlak tertutup dari publik"},
    {"Regulasi": "UU 14/2008 (KIP)", "Pasal": "Pasal 17 huruf a & d", "Klasifikasi": "Informasi Publik Dikecualikan", "Substansi": "Wajib dikecualikan melalui pengujian konsekuensi PPID"}
]
with open(f"{target_dir}/kerahasiaan_arsip_musyawarah.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t6[0].keys()); w.writeheader(); w.writerows(t6)

# 7. Harmonisasi Draf PERMA (Pasal 1, 2, 3)
t7 = [
    {"Pasal_Draf": "Pasal 1", "Uji": "Vertikal & Horizontal", "Isu": "Definisi SIP, Dissenting & Concurring Opinion", "Rekomendasi": "Hindari norma operasional terselubung di pasal ketentuan umum"},
    {"Pasal_Draf": "Pasal 2", "Uji": "Vertikal (UU 48/2009 & KUHP)", "Isu": "Batas Sanksi Kerahasiaan & Rahasia Jabatan", "Rekomendasi": "Batasi sanksi pada disiplin/etik; delegasikan SOP teknis ke SK KMA"},
    {"Pasal_Draf": "Pasal 3", "Uji": "Vertikal (KUHAP, UU ITE, PDP)", "Isu": "Legalitas TTE Putusan & Akses Berjenjang", "Rekomendasi": "Gunakan TTE tersertifikasi dan tegaskan minutasi tertulis jika ada deviasi"}
]
with open(f"{target_dir}/harmonisasi_draf_perma.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=t7[0].keys()); w.writeheader(); w.writerows(t7)

print(" All 10 judicial deliberation and regulatory datasets exported successfully to CSV!")
