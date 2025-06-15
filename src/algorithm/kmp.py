class KMP:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.prefix_table = self._build_prefix_table()

    def _build_prefix_table(self) -> list[int]:
        m = len(self.pattern)
        lps = [0] * m
        length = 0
        i = 1
        
        while i < m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    def search(self, text: str) -> list[int]:
        n = len(text)
        m = len(self.pattern)
        
        if m == 0: return []
        if n == 0: return []
        if m > n: return []

        lps = self.prefix_table
        occurrences = []
        
        i = 0 
        j = 0 
        
        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                occurrences.append(i - j) 
                j = lps[j - 1] 
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
                    
        return occurrences

    def count_occurrences(self, text: str) -> int:
        return len(self.search(text))