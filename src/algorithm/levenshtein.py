import re
from collections import Counter

class Levenshtein:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def _calculate_distance(self, s1: str, s2: str) -> int:
        len_s1, len_s2 = len(s1), len(s2)
        if len_s1 > len_s2:
            s1, s2 = s2, s1
            len_s1, len_s2 = len_s2, len_s1

        dp_row = list(range(len_s1 + 1))
        for i in range(1, len_s2 + 1):
            prev_dp_val = dp_row[0]
            dp_row[0] = i
            for j in range(1, len_s1 + 1):
                temp = dp_row[j]
                cost = 0 if s2[i-1] == s1[j-1] else 1
                dp_row[j] = min(dp_row[j] + 1, dp_row[j-1] + 1, prev_dp_val + cost)
                prev_dp_val = temp
        return dp_row[len_s1]

    def similarity(self, word1: str, word2: str) -> float:
        distance = self._calculate_distance(word1.lower(), word2.lower())
        max_len = max(len(word1), len(word2))
        if max_len == 0:
            return 1.0
        return 1.0 - (distance / max_len)

    def is_similar(self, word1: str, word2: str) -> bool:
        return self.similarity(word1, word2) >= self.threshold

    def find_similar_keywords(self, keywords: list[str], text: str) -> dict[str, Counter]:
        words_in_text = re.findall(r'\b\w+\b', text.lower())
        
        similar_matches = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            found_words = [
                text_word for text_word in words_in_text 
                if self.is_similar(keyword_lower, text_word)
            ]
            
            if found_words:
                similar_matches[keyword] = Counter(found_words)
                
        return similar_matches