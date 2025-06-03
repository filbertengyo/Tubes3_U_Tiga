import fitz  

class PDFParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text(self) -> str:
        """
        Membaca seluruh halaman PDF dan menggabungkannya menjadi satu string.
        Return: teks lengkap dari dokumen.
        """
        text = ""
        with fitz.open(self.pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
