class SearchPage:
    def __init__(self, parent):
        """
        Inisialisasi halaman pencarian.

        Parameters:
        - parent: Referensi ke MainWindow atau root window.
        """
        pass

    def setup_widgets(self):
        """
        Menyusun semua widget GUI seperti input keyword, dropdown algoritma, dll.
        """
        pass

    def get_keywords(self) -> list[str]:
        """
        Mengambil keyword dari input user dan mengembalikan dalam bentuk list string.

        Returns:
        - List of keyword string
        """
        pass

    def get_algorithm(self) -> str:
        """
        Mengembalikan algoritma string matching yang dipilih user (KMP / BM).

        Returns:
        - "KMP" atau "BM"
        """
        pass

    def get_top_n(self) -> int:
        """
        Mengembalikan jumlah maksimum CV yang ingin ditampilkan.

        Returns:
        - Integer jumlah top-N
        """
        pass

    def display_results(self, results: list[dict]):
        """
        Menampilkan hasil pencarian ke dalam container GUI.

        Parameters:
        - results (list of dict): List berisi data hasil pencocokan tiap CV.
        """
        pass

    def on_search_clicked(self):
        """
        Fungsi yang dipanggil saat tombol Search ditekan.
        Bertugas membaca input, memanggil backend, dan menampilkan hasil.
        """
        pass
