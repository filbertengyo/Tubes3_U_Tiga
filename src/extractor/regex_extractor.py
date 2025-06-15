import re
from typing import Dict

class RegexExtractor:
    def __init__(self, raw_text: str):
        self.text = raw_text

    def extract_email(self) -> str:
        # Cari satu email yang paling masuk akal (pola standar)
        return self._match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def extract_phone(self) -> str:
        # Pola untuk nomor telepon internasional + lokal (US/ID)
        return self._match(r"(\+?\d{1,3}[-.\s]?)?(0|62)?[1-9][0-9]{7,12}")

    def extract_name(self) -> str:
        # Ambil baris pertama sebagai nama jika panjangnya wajar
        first_line = self.text.strip().split('\n')[0]
        if 2 <= len(first_line.split()) <= 5:
            return first_line.strip()
        return ""

    def extract_skills(self) -> list[str]:
        # Mengambil bagian "Skills" atau kata-kata yang mirip sebagai acuan
        skill_block = self._block("skills?")
        return re.findall(r"\b[A-Za-z\+\#]{2,}(?: [A-Za-z\+]{2,})?\b", skill_block)

    def extract_education(self) -> list[str]:
        # Ambil semua baris dari bagian 'Education' sampai kosong / baris non-relevan
        return re.findall(r"(Associate|Bachelor|Master|BSN|Ph\.?D|S1|S2|University|College|Degree).*", self.text, re.IGNORECASE)

    def extract_experience(self) -> list[str]:
        # Ambil semua baris yang menunjukkan format waktu kerja
        return re.findall(r"(?i)(\b(January|February|March|April|May|June|July|August|September|October|November|December)\b)?\s*\d{4}\s*(to|-|–)\s*(Present|\d{4})", self.text)

    def extract_all(self) -> Dict[str, any]:
        return {
            "name": self.extract_name(),
            "email": self.extract_email(),
            "phone": self.extract_phone(),
            "skills": self.extract_skills(),
            "education": self.extract_education(),
            "experience": self.extract_experience()
        }

    def _match(self, pattern: str) -> str:
        match = re.search(pattern, self.text)
        return match.group() if match else ""

    def _block(self, heading_keyword: str) -> str:
        """
        Mengambil blok teks di bawah heading tertentu (seperti 'Skills', 'Summary', 'Education')
        """
        pattern = rf"{heading_keyword}.*?\n(.*?)(\n\n|\n[A-Z][a-z])"
        match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else ""
