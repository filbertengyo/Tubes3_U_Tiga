from .pdf_parser import PDFParser
from .regex_extractor import RegexExtractor
from typing import Dict

class CVProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""

    def process(self) -> Dict[str, any]:
        """Mengekstrak teks dari PDF dan mengambil informasi penting."""
        self.text = PDFParser(self.pdf_path).extract_text()
        extractor = RegexExtractor(self.text)
        return extractor.extract_all()

    def get_raw_text(self) -> str:
        """Return teks CV mentah setelah diekstrak dari PDF."""
        if not self.text:
            self.text = PDFParser(self.pdf_path).extract_text()
        return self.text
