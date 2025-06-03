class KMP:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.prefix_table = self._build_prefix_table()

    def _build_prefix_table(self) -> list[int]:
        """Membangun tabel prefix (pi table) untuk pattern."""
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
