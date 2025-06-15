from src.extractor.pdf_parser import PDFParser
from src.extractor.regex_extractor import RegexExtractor
from typing import Any

class CVProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""

    def process(self) -> str:
        """Mengekstrak teks dari PDF dan mengambil informasi penting."""
        self.text = PDFParser(self.pdf_path).extract_text()
        return RegexExtractor(self.text).extract_all()

    def get_raw_text(self) -> str:
        """Return teks CV mentah setelah diekstrak dari PDF."""
        if not self.text:
            self.text = PDFParser(self.pdf_path).extract_text()
        return self.text
