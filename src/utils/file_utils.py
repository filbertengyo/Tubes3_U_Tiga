import os

def is_pdf_file(path: str) -> bool:
    """Memastikan file berformat PDF dan eksis"""
    return os.path.isfile(path) and path.lower().endswith(".pdf")

def get_filename(path: str) -> str:
    """Mendapatkan nama file dari path"""
    return os.path.basename(path)
