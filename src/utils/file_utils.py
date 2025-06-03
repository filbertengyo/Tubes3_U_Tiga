import os

def is_pdf_file(path: str) -> bool:
    """Memastikan file berformat PDF dan eksis"""
    return os.path.isfile(path) and path.lower().endswith(".pdf")

def list_pdf_files(folder_path: str) -> list[str]:
    """Mengembalikan semua path file PDF dari folder"""
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if is_pdf_file(os.path.join(folder_path, f))
    ]

def get_filename(path: str) -> str:
    """Mendapatkan nama file dari path"""
    return os.path.basename(path)
