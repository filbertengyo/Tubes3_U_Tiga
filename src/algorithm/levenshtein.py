class Levenshtein:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def _calculate_distance(self, s1: str, s2: str) -> int:
        len_s1 = len(s1)
        len_s2 = len(s2)

        dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

        for i in range(len_s1 + 1):
            dp[i][0] = i
        for j in range(len_s2 + 1):
            dp[0][j] = j

        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                
                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + cost
                )
        
        return dp[len_s1][len_s2]

    def similarity(self, word1: str, word2: str) -> float:
        distance = self._calculate_distance(word1.lower(), word2.lower())
        max_len = max(len(word1), len(word2))
        
        if max_len == 0:
            return 1.0
        
        return 1.0 - (distance / max_len)

    def is_similar(self, word1: str, word2: str) -> bool:
        return self.similarity(word1, word2) >= self.threshold

    def find_similar_keywords(self, keywords: list[str], text: str) -> dict[str, list[int]]:
        words_in_text = text.lower().split()
        
        similar_matches = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            matching_indices = []
            
            for i, text_word in enumerate(words_in_text):
                if self.is_similar(keyword_lower, text_word):
                    matching_indices.append(i)
            
            if matching_indices:
                similar_matches[keyword] = matching_indices
                
        return similar_matches