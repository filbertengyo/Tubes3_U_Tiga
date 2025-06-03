import re
from typing import Dict

class RegexExtractor:
    def __init__(self, raw_text: str):
        self.text = raw_text

    def extract_email(self) -> str:
        return self._match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def extract_phone(self) -> str:
        return self._match(r"(\+62|62|0)[0-9]{9,12}")

    def extract_name(self) -> str:
        # Bisa disesuaikan lebih cerdas, contoh: ambil baris pertama
        return self.text.strip().split("\n")[0]

    def extract_skills(self) -> list[str]:
        return re.findall(r"\b(?:Python|React|SQL|JavaScript|Node|HTML|CSS)\b", self.text, re.IGNORECASE)

    def extract_education(self) -> list[str]:
        return re.findall(r"(S1|S2|Bachelor|Master|Universitas|University).*", self.text, re.IGNORECASE)

    def extract_experience(self) -> list[str]:
        return re.findall(r"(?i)(\d{4})\s*-\s*(\d{4}|Present).*", self.text)

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
