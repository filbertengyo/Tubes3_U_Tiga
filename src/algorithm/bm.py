class BM:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.m = len(pattern)
        self.bad_char_table = self._build_bad_char_table()
        self.good_suffix_shifts_case1, self.good_suffix_shifts_case2 = self._build_good_suffix_table()

    def _build_bad_char_table(self) -> list[int]:
        bad_char = [-1] * 256 
        for i in range(self.m):
            bad_char[ord(self.pattern[i])] = i
        return bad_char

    def _build_good_suffix_table(self) -> tuple[list[int], list[int]]:
        shifts = [self.m] * (self.m + 1)
        
        border_array = [0] * (self.m + 1) 
        
        j = 0
        for i in range(1, self.m):
            while j > 0 and self.pattern[i] != self.pattern[j]:
                j = border_array[j - 1]
            if self.pattern[i] == self.pattern[j]:
                j += 1
            border_array[i] = j
        
        for i in range(self.m):
            shifts[border_array[i]] = self.m - 1 - i

        j = 0
        for i in range(self.m - 1, -1, -1):
            if border_array[i] == i + 1: 
                for k in range(j, self.m - 1 - i):
                    if shifts[k] == self.m: 
                        shifts[k] = self.m - 1 - i
                j = self.m - 1 - i
        
        return shifts, border_array

    def search(self, text: str) -> list[int]:
        n = len(text)
        m = self.m
        
        if m == 0: return []
        if n == 0: return []
        if m > n: return []

        bad_char_table = self.bad_char_table
        good_suffix_shifts, _ = self.good_suffix_shifts_case1 

        occurrences = []
        s = 0 

        while s <= (n - m):
            j = m - 1 
            
            while j >= 0 and self.pattern[j] == text[s + j]:
                j -= 1
            
            if j < 0:
                occurrences.append(s)
                s += good_suffix_shifts[0] if good_suffix_shifts[0] != self.m else 1
            else:
                char_at_text_code = ord(text[s + j])
                
                shift_bc = j - bad_char_table[char_at_text_code]
                
                shift_gs = good_suffix_shifts[j + 1]
                
                s += max(shift_bc, shift_gs)
                
        return occurrences

    def count_occurrences(self, text: str) -> int:
        return len(self.search(text))