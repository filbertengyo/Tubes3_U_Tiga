class SummaryPage:
    def __init__(self, parent):
        """
        Inisialisasi halaman ringkasan CV.

        Parameters:
        - parent: Referensi ke MainWindow atau root window.
        """
        pass

    def setup_widgets(self):
        """
        Menyusun elemen UI untuk ringkasan CV seperti nama, email, pengalaman, dsb.
        """
        pass

    def load_applicant(self, applicant_data: dict):
        """
        Menampilkan detail informasi dari pelamar terpilih.

        Parameters:
        - applicant_data (dict): Hasil ekstraksi informasi dari satu CV.
        """
        pass

    def on_view_cv(self):
        """
        Membuka file CV asli menggunakan viewer default (PDF reader).
        """
        pass

    def on_back(self):
        """
        Kembali ke halaman pencarian dari ringkasan CV.
        """
        pass
