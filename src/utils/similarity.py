from src.algorithm.levenshtein import *

def fuzzy_match_keywords(keywords: list[str], text: str, threshold: float = 0.8) -> dict[str, list[str]]:
    """
    Untuk setiap keyword, cari kata dalam teks yang mirip.
    Return dict keyword → list kata dalam teks yang mirip.
    """
    words_in_text = set(text.lower().split())
    matcher = Levenshtein(threshold)
    result = {}

    for keyword in keywords:
        keyword_lower = keyword.lower()
        result[keyword] = [
            word for word in words_in_text if matcher.is_similar(keyword_lower, word)
        ]

    return result
