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
from collections import Counter

class SearchWorker(QObject):
    search_finished = pyqtSignal(list, float, float)
    search_error = pyqtSignal(str)
    
    def __init__(self, keywords: list[str], algorithm: str, top_n: int):
        super().__init__()
        self.keywords = [k.strip() for k in keywords]
        self.algorithm = algorithm
        self.top_n = top_n
        self.is_cancelled = False

    def run(self):
        timer = Timer()
        try:
            all_cv_tuples = get_all_applications()
            print(len(all_cv_tuples))
        except Exception as e:
            self.search_error.emit(f"Database connection error: {e}")
            return

        timer.start()
        exact_results_list = []
        processed_cv_paths = set()
        
        if self.algorithm == "AhoCorasick":
            ac = AhoCorasick()
            for k in self.keywords:
                ac.add_pattern(k.lower())
            ac.build_failure_links()

        for cv_tuple in all_cv_tuples:
            if self.is_cancelled: return
            applicant_id, first_name, last_name, dob, address, phone, cv_path, _, detail_id = cv_tuple
            
            if not cv_path or not os.path.exists(cv_path):
                print(cv_path)
                print("GA ADA ANJAY")
                continue

            if cv_path in processed_cv_paths:
                print(cv_path)
                print("Udah di cek anjay")
            
            raw_text = PDFParser(cv_path).extract_text()
            if not raw_text: continue
            
            search_text = raw_text.lower()
            found_matches = {}

            if self.algorithm == "AhoCorasick":
                matches = ac.search(search_text)
                for _, pattern in matches:
                    original_keyword = next((k for k in self.keywords if k.lower() == pattern), pattern)
                    found_matches[original_keyword] = found_matches.get(original_keyword, 0) + 1
            else:
                for keyword in self.keywords:
                    matcher = KMP(keyword.lower()) if self.algorithm == "KMP" else BM(keyword.lower())
                    count = matcher.count_occurrences(search_text)
                    if count > 0:
                        found_matches[keyword] = count

            if found_matches:
                processed_cv_paths.add(cv_path)
                exact_results_list.append({
                    'applicant_id': applicant_id, 'name': f"{first_name} {last_name}".strip(),
                    'date_of_birth': dob, 'address': address, 'phone_number': phone,
                    'cv_path': cv_path, 'matched_keywords': found_matches,
                    'raw_text': raw_text
                })
        
        timer.stop()
        exact_time_ms = timer.elapsed_ms()
        fuzzy_time_ms = 0.0
        
        final_results_list = exact_results_list

        if len(final_results_list) < self.top_n:
            timer.start()
            fuzzy_thresholds = [0.75, 0.5, 0.25]

            for threshold in fuzzy_thresholds:
                if len(final_results_list) >= self.top_n or self.is_cancelled:
                    break
                
                fuzzy_matcher = Levenshtein(threshold=threshold)
                
                remaining_cvs = [cv for cv in all_cv_tuples if cv[6] not in processed_cv_paths]

                for cv_tuple in remaining_cvs:
                    if len(final_results_list) >= self.top_n or self.is_cancelled:
                        break

                    applicant_id, first_name, last_name, dob, address, phone, cv_path, _, detail_id= cv_tuple
                    
                    if not cv_path or not os.path.exists(cv_path): continue
                    raw_text = PDFParser(cv_path).extract_text()
                    if not raw_text: continue
                    
                    similar_found = fuzzy_matcher.find_similar_keywords(self.keywords, raw_text)
                    
                    if similar_found:
                        processed_cv_paths.add(cv_path)
                        res_entry = {
                            'applicant_id': applicant_id, 'name': f"{first_name} {last_name}".strip(),
                            'date_of_birth': dob, 'address': address, 'phone_number': phone,
                            'cv_path': cv_path, 'matched_keywords': {},
                            'raw_text': raw_text
                        }
                        
                        for keyword, found_counter in similar_found.items():
                            for found_word, count in found_counter.items():
                                key = f"{keyword} (fuzzy: '{found_word}')"
                                res_entry['matched_keywords'][key] = count
                        
                        final_results_list.append(res_entry)

            timer.stop()
            fuzzy_time_ms = timer.elapsed_ms()

        for res in final_results_list:
            res['match_count'] = sum(res.get('matched_keywords', {}).values())

        final_results_list.sort(key=lambda x: x.get('match_count', 0), reverse=True)
        
        self.search_finished.emit(final_results_list[:self.top_n], exact_time_ms, fuzzy_time_ms)

    def cancel(self):
        self.is_cancelled = True
