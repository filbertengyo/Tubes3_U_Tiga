import os
from PyQt6.QtCore import QObject, pyqtSignal
from src.database.query import get_all_applications
from src.extractor.pdf_parser import PDFParser
from src.algorithm.kmp import KMP
from src.algorithm.bm import BM
from src.algorithm.levenshtein import Levenshtein
from src.algorithm.aho_corasick import AhoCorasick
from src.utils.timer import Timer
from src.extractor.regex_extractor import RegexExtractor

class SearchWorker(QObject):
    search_finished = pyqtSignal(list, float, float)
    search_error = pyqtSignal(str)
    
    def __init__(self, keywords: list[str], algorithm: str, top_n: int):
        super().__init__()
        self.keywords = keywords
        self.algorithm = algorithm
        self.top_n = top_n
        self.is_cancelled = False

    def run(self):
        timer = Timer()
        try:
            all_cv_tuples = get_all_applications()
        except Exception as e:
            self.search_error.emit(f"Database connection error: {e}")
            return

        timer.start()
        results_dict = {}
        globally_found_keywords = set()

        if self.algorithm == "AhoCorasick":
            ac = AhoCorasick()
            for k in self.keywords:
                ac.add_pattern(k)
            ac.build_failure_links()

        for cv_tuple in all_cv_tuples:
            if self.is_cancelled:
                return

            applicant_id, first_name, last_name, dob, address, phone, cv_path, _ = cv_tuple

            if not cv_path or not os.path.exists(cv_path):
                continue

            raw_text = PDFParser(cv_path).extract_text()
            if not raw_text:
                continue

            search_text = raw_text.lower()
            found_matches = {}

            if self.algorithm == "AhoCorasick":
                matches = ac.search(search_text)
                for _, pattern in matches:
                    original_keyword = next((k for k in self.keywords if k.lower() == pattern), pattern)
                    found_matches[original_keyword] = found_matches.get(original_keyword, 0) + 1
            else:
                for keyword in self.keywords:
                    matcher = KMP(keyword) if self.algorithm == "KMP" else BM(keyword)
                    count = matcher.count_occurrences(search_text)
                    if count > 0:
                        found_matches[keyword] = count

            if found_matches:
                globally_found_keywords.update(found_matches.keys())
                regex = RegexExtractor(raw_text)
                summary_data = regex.extract_all()
                results_dict[applicant_id] = {
                    'applicant_id': applicant_id,
                    'name': f"{first_name} {last_name}".strip(),
                    'date_of_birth': dob,
                    'address': address,
                    'phone_number': phone,
                    'cv_path': cv_path,
                    'matched_keywords': found_matches,
                    'summary': summary_data
                }
        
        timer.stop()
        exact_time_ms = timer.elapsed_ms()

        unfound_keywords = [k for k in self.keywords if k not in globally_found_keywords]
        fuzzy_time_ms = 0.0

        if unfound_keywords:
            timer.start()
            fuzzy_matcher = Levenshtein(threshold=0.85)

            for cv_tuple in all_cv_tuples:
                if self.is_cancelled:
                    return

                applicant_id, first_name, last_name, dob, address, phone, cv_path, _ = cv_tuple
                res_entry = results_dict.get(applicant_id)

                if res_entry:
                    continue 

                if not cv_path or not os.path.exists(cv_path):
                    continue
                
                raw_text = PDFParser(cv_path).extract_text()
                if not raw_text:
                    continue
                
                similar_found = fuzzy_matcher.find_similar_keywords(unfound_keywords, raw_text)

                if similar_found:
                    summary_data = RegexExtractor(raw_text).extract_all()
                    res_entry = {
                        'applicant_id': applicant_id,
                        'name': f"{first_name} {last_name}".strip(),
                        'date_of_birth': dob,
                        'address': address,
                        'phone_number': phone,
                        'cv_path': cv_path,
                        'matched_keywords': {},
                        'summary': summary_data
                    }
                    results_dict[applicant_id] = res_entry

                    for keyword, matches in similar_found.items():
                        res_entry['matched_keywords'][f"{keyword} (fuzzy)"] = len(matches)

            timer.stop()
            fuzzy_time_ms = timer.elapsed_ms()

        final_results = list(results_dict.values())
        for res in final_results:
            res['match_count'] = len(res['matched_keywords'])

        final_results.sort(key=lambda x: x.get('match_count', 0), reverse=True)

        self.search_finished.emit(final_results[:self.top_n], exact_time_ms, fuzzy_time_ms)

    def cancel(self):
        self.is_cancelled = True
