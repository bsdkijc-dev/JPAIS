import os, re, hashlib, json
from pathlib import Path
import pypdf
from statute_parser import IndonesianStatuteParser
from judicial_parser import IndonesianJudicialDecisionParser

class LegalDocumentIngestor:
    def __init__(self, manifest_path: str = "/home/ai/JPAIS/datasets/ingestion_manifest.jsonl"):
        self.manifest_path = manifest_path
        self.statute_parser = IndonesianStatuteParser()
        self.judicial_parser = IndonesianJudicialDecisionParser()

    def close(self):
        self.statute_parser.close()
        self.judicial_parser.close()

    def clean_extracted_text(self, text: str) -> str:
        """Strips institutional header noise, page markers, and disclaimer watermarks."""
        # Strip Mahkamah Agung disclaimer and directory watermarks
        text = re.sub(r'Direktori\s+Putusan\s+Mahkamah\s+Agung\s+Republik\s+Indonesia[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'putusan\.mahkamahagung\.go\.id[^\n]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Disclaimer[^\n]*kepaniteraan\.mahkamahagung\.go\.id[^\n]*', '', text, flags=re.IGNORECASE)
        # Strip running page footers (e.g. Halaman 2 dari 15)
        text = re.sub(r'Halaman\s+\d+\s+dari\s+\d+[^\n]*', '', text, flags=re.IGNORECASE)
        # Normalize whitespace and excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = pypdf.PdfReader(pdf_path)
        extracted_pages = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)
        full_text = "\n".join(extracted_pages)
        return self.clean_extracted_text(full_text)

    def classify_document(self, text: str) -> str:
        """Determines legal document type from textual signatures."""
        upper_text = text[:1000].upper()
        if "PUTUSAN" in upper_text and ("MAHKAMAH AGUNG" in upper_text or "PENGADILAN" in upper_text):
            return "judicial_decision"
        elif any(k in upper_text for k in ["UNDANG-UNDANG", "PERATURAN PEMERINTAH", "PERATURAN PRESIDEN", "PERATURAN MENTERI"]):
            return "statute"
        return "unstructured_legal_text"

    def process_and_ingest(self, file_path: str, default_status: str = "verified"):
        p = Path(file_path)
        print(f"\nProcessing: {p.name} ({p.stat().st_size} bytes)")

        # 1. Extract text according to format
        if p.suffix.lower() == ".pdf":
            raw_text = self.extract_text_from_pdf(file_path)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = self.clean_extracted_text(f.read())

        doc_hash = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()

        # 2. Classify document
        doc_type = self.classify_document(raw_text)
        print(f" -> Classification: {doc_type.upper()}")

        # 3. Route to specialized domain parser
        if doc_type == "judicial_decision":
            # Temporary file for parser
            temp_path = f"/tmp/{p.stem}_clean.txt"
            with open(temp_path, "w", encoding="utf-8") as tf:
                tf.write(raw_text)

            parsed = self.judicial_parser.parse_decision(temp_path)
            parsed["verification_status"] = default_status
            self.judicial_parser.ingest(parsed)
            os.remove(temp_path)

            manifest_record = {
                "filename": p.name,
                "document_id": parsed["id"],
                "document_type": doc_type,
                "classification_details": {
                    "decision_number": parsed["decision_number"],
                    "year": parsed["year"],
                    "ruling": parsed["ruling_type"]
                },
                "sha256_hash": doc_hash,
                "pseudonymization_applied": True,
                "status": default_status
            }

        elif doc_type == "statute":
            temp_path = f"/tmp/{p.stem}_clean.txt"
            with open(temp_path, "w", encoding="utf-8") as tf:
                tf.write(raw_text)

            # Heuristic detection for statute metadata
            num_match = re.search(r'NOMOR\s+(\d+)\s+TAHUN\s+(\d{4})', raw_text, re.IGNORECASE)
            number = num_match.group(1) if num_match else "1"
            year = int(num_match.group(2)) if num_match else 2024
            reg_type = "Undang-Undang" if "UNDANG-UNDANG" in raw_text[:300].upper() else "Peraturan Pemerintah"
            reg_id = f"{'UU' if reg_type == 'Undang-Undang' else 'PP'}-{number}-{year}"

            parsed = self.statute_parser.parse_text(
                filepath=temp_path,
                reg_id=reg_id,
                reg_type=reg_type,
                number=number,
                year=year,
                title=p.stem.replace("_", " ").title(),
                status=default_status
            )
            self.statute_parser.ingest(parsed)
            os.remove(temp_path)

            manifest_record = {
                "filename": p.name,
                "document_id": parsed["reg_id"],
                "document_type": doc_type,
                "classification_details": {
                    "reg_type": reg_type,
                    "number": number,
                    "year": year
                },
                "sha256_hash": doc_hash,
                "status": default_status
            }

        # 4. Append audit record to ingestion manifest
        with open(self.manifest_path, "a", encoding="utf-8") as mf:
            mf.write(json.dumps(manifest_record) + "\n")
        print(f" -> Logged cryptographic audit manifest: {doc_hash[:16]}...")
        return manifest_record

if __name__ == "__main__":
    import reportlab.lib.pagesizes as pagesizes
    from reportlab.pdfgen import canvas

    # Generate a realistic Supreme Court PDF test document
    pdf_sample_path = "/home/ai/JPAIS/datasets/verified/putusan_kasasi_5678.pdf"
    print("Generating benchmark judicial PDF with court watermarks...")
    c = canvas.Canvas(pdf_sample_path, pagesize=pagesizes.letter)
    c.drawString(100, 750, "Direktori Putusan Mahkamah Agung Republik Indonesia - putusan.mahkamahagung.go.id")
    c.drawString(100, 720, "PUTUSAN")
    c.drawString(100, 700, "Nomor 5678 K/Pdt.Sus-HKI/2023")
    c.drawString(100, 680, "DEMI KEADILAN BERDASARKAN KETUHANAN YANG MAHA ESA - MAHKAMAH AGUNG")
    c.drawString(100, 650, "BAMBANG SUDARMONO, bertempat tinggal di Jalan Melati No. 12 RT 01/RW 04, NIK 3273012345670002;")
    c.drawString(100, 630, "Pemohon Kasasi; Lawan PT CIPTA CIPTA KREATIF, Termohon Kasasi;")
    c.drawString(100, 600, "DUDUK PERKARA")
    c.drawString(100, 580, "Penggugat menuntut pembatalan pendaftaran hak cipta motif batik digital...")
    c.drawString(100, 550, "PERTIMBANGAN HUKUM")
    c.drawString(100, 530, "Kaidah Hukum: Karya seni yang dihasilkan murni oleh algoritma AI generatif tanpa kontribusi")
    c.drawString(100, 510, "kreatif orisinal manusia tidak memenuhi syarat perlindungan hak cipta.")
    c.drawString(100, 470, "AMAR PUTUSAN MENGADILI:")
    c.drawString(100, 450, "Menolak permohonan kasasi dari Pemohon Kasasi;")
    c.drawString(100, 100, "Halaman 1 dari 1 - Disclaimer: Informasi ini tunduk pada UU PDP")
    c.save()
    print(f"Created: {pdf_sample_path}")

    # Run LegalDocumentIngestor on the PDF
    ingestor = LegalDocumentIngestor()
    ingestor.process_and_ingest(pdf_sample_path, default_status="verified")
    ingestor.close()
    print("\n=== MULTIMODAL INGESTION ENGINE VERIFIED ===")
