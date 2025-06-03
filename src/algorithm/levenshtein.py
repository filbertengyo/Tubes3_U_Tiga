class Levenshtein:
    def __init__(self, threshold: float = 0.8):
        """
        threshold: nilai kemiripan minimum (0.0 - 1.0)
        """
        self.threshold = threshold

    def similarity(self, word1: str, word2: str) -> float:
        """
        Menghitung similarity antara dua string menggunakan
        Levenshtein distance → nilai antara 0.0 - 1.0
        """
        pass

    def is_similar(self, word1: str, word2: str) -> bool:
        """Return True jika similarity >= threshold"""
        return self.similarity(word1, word2) >= self.threshold

    def find_similar_keywords(self, keywords: list[str], text: str) -> dict[str, list[int]]:
        """
        Untuk setiap keyword, cari semua posisi kata dalam text
        yang mirip dengan keyword (berdasarkan threshold).
        Return dict keyword → list of index match.
        """
        pass
