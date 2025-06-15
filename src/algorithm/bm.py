class BM:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.m = len(pattern)
        if self.m > 0:
            self.bad_char_table = self._build_bad_char_table()
            self.good_suffix_shifts = self._build_good_suffix_table()

    def _build_bad_char_table(self) -> dict:
        bad_char = {}
        for i in range(self.m):
            bad_char[self.pattern[i]] = i
        return bad_char

    def _build_good_suffix_table(self) -> list[int]:
        m = self.m
        shifts = [0] * (m + 1)
        border_pos = [0] * (m + 1)

        i = m
        j = m + 1
        border_pos[i] = j
        while i > 0:
            while j <= m and self.pattern[i - 1] != self.pattern[j - 1]:
                if shifts[j] == 0:
                    shifts[j] = j - i
                j = border_pos[j]
            i -= 1
            j -= 1
            border_pos[i] = j

        j = border_pos[0]
        for i in range(m + 1):
            if shifts[i] == 0:
                shifts[i] = j
            if i == j:
                j = border_pos[j]
        
        return shifts

    def search(self, text: str) -> list[int]:
        n = len(text)
        m = self.m
        
        if m == 0 or n == 0 or m > n:
            return []

        occurrences = []
        s = 0

        while s <= (n - m):
            j = m - 1
            
            while j >= 0 and self.pattern[j] == text[s + j]:
                j -= 1
            
            if j < 0:
                occurrences.append(s)
                s += self.good_suffix_shifts[0]
            else:
                char_in_text = text[s + j]
                last_occurrence = self.bad_char_table.get(char_in_text, -1)
                
                bad_char_shift = j - last_occurrence
                good_suffix_shift = self.good_suffix_shifts[j + 1]
                
                s += max(1, bad_char_shift, good_suffix_shift)
                
        return occurrences

    def count_occurrences(self, text: str) -> int:
        return len(self.search(text))