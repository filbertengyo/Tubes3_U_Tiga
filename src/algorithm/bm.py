class BM:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.bad_char_table = self._build_bad_char_table()
        self.good_suffix_table = self._build_good_suffix_table()

    def _build_bad_char_table(self) -> dict:
        """Membangun tabel bad character rule."""
        pass

    def _build_good_suffix_table(self) -> list[int]:
        """Membangun tabel good suffix rule."""
        pass

    def search(self, text: str) -> list[int]:
        """
        Melakukan pencarian pattern dalam text.
        Return: list indeks awal match.
        """
        pass

    def count_occurrences(self, text: str) -> int:
        """Mengembalikan jumlah kemunculan pattern dalam text."""
        return len(self.search(text))
