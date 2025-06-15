import re
from typing import Dict, List, Any

class RegexExtractor:
    def __init__(self, raw_text: str):
        self.text = raw_text
    
    def extract_all(text: str) -> str:
        all_info = {}
    
        text = re.sub(r'\s{2,}', ' ', text)
        text = re.sub(r'\n{2,}', '\n', text)

        job_title_pattern = r'^(?:--- PAGE \d+ ---\n)?\s*([A-Z][A-Z\s.-]+)(?=\n[A-Z][a-z]+|\nSkill|\nSummary|\nObjective|$)'
        job_title_match = re.search(job_title_pattern, text, re.MULTILINE)
        if job_title_match:
            all_info['Job_Title'] = job_title_match.group(1).strip()
            all_info['Job_Title'] = re.sub(r'[•Â$]', '', all_info['Job_Title']).strip()
            all_info['Job_Title'] = re.sub(r'\s+', ' ', all_info['Job_Title']).strip()
        
        #Cari skills
        skills_pattern = r'Skills\s*\n*(.*?)(?=\n\s*[A-Z][a-z]+\s*|\Z)'
        skills_match = re.search(skills_pattern, text, re.DOTALL | re.IGNORECASE)
        if skills_match:
            skills_text = skills_match.group(1).strip()
            skills_text = re.sub(r'\n+', ' ', skills_text)
            skills_text = re.sub(r'\s+', ' ', skills_text)
            skills_text = re.sub(r'[•-]', '', skills_text).strip()
            all_info['Skills'] = skills_text
        
        #Cari summary
        summary_pattern = r'Summary\s*\n+(.*?)(?=\n\s*[A-Z][a-z]+\s*\n|$)'
        summary_match = re.search(summary_pattern, text, re.DOTALL | re.IGNORECASE)
        if summary_match:
            summary_text = summary_match.group(1).strip()
            summary_text = re.sub(r'\n+', ' ', summary_text)
            summary_text = re.sub(r'\s+', ' ', summary_text)
            summary_text = re.sub(r'[•Â$]', '', summary_text).strip()
            all_info['Summary'] = summary_text
        
        #Cari highlights
        highlights_pattern = r'Highlights\s*\n+(.*?)(?=\n\s*[A-Z][a-z]+\s*\n|$)'
        highlights_match = re.search(highlights_pattern, text, re.DOTALL | re.IGNORECASE)
        if highlights_match:
            highlights_text = highlights_match.group(1).strip()
            highlights_text = re.sub(r'\n+', ' ', highlights_text)
            highlights_text = re.sub(r'\s+', ' ', highlights_text)
            highlights_text = re.sub(r'[•Â$]', '', highlights_text).strip()
            all_info['Highlights'] = highlights_text
        
        #Cari accomplishments
        accomplishments_pattern = r'Accomplishments\s*\n+(.*?)(?=\n\s*[A-Z][a-z]+\s*\n|$)'
        accomplishments_match = re.search(accomplishments_pattern, text, re.DOTALL | re.IGNORECASE)
        if accomplishments_match:
            accomplishments_text = accomplishments_match.group(1).strip()
            accomplishments_text = re.sub(r'\n+', ' ', accomplishments_text)
            accomplishments_text = re.sub(r'\s+', ' ', accomplishments_text)
            accomplishments_text = re.sub(r'[•Â$]', '', accomplishments_text).strip()
            all_info['Accomplishments'] = accomplishments_text
        
        #Cari work experiences
        experience_pattern = r'Experience\s*\n+(.*?)(?=\n\s*Education|\n\s*Certifications|\n\s*Interests|\n\s*Additional Information|\Z)'
        experience_match = re.search(experience_pattern, text, re.DOTALL | re.IGNORECASE)
        
        final_job_entries = []
        
        if experience_match:
            experience_block = experience_match.group(1).strip()
            experience_block = re.sub(r'\n{2,}', '\n', experience_block)

            job_entry_pattern = r'(\d{2}/\d{4}\s*(?:to|-)\s*(?:Current|Present|\d{2}/\d{4}))\s*(.*?)(?=\n*\d{2}/\d{4}\s*(?:to|-)\s*(?:Current|Present|\d{2}/\d{4})|\Z)'
            raw_job_matches = re.findall(job_entry_pattern, experience_block, re.DOTALL | re.IGNORECASE)

            for date_range, job_content_block in raw_job_matches:
                current_job_dict = {
                    'Date': date_range.strip(),
                    'Company': 'N/A',
                    'Position': 'N/A',
                }
                
                lines_in_block = [line.strip() for line in job_content_block.split('\n') if line.strip()]

                if lines_in_block:
                    company_found_index = -1
                    for i, line_content in enumerate(lines_in_block):
                        if "Company Name" in line_content or re.match(r'^[A-Z][a-zA-Z\s-]+(?: LLC| Inc\.| Corp\.)?$', line_content):
                            current_job_dict['Company'] = re.sub(r'(?: - City, State| City, State)?', '', line_content).strip()
                            current_job_dict['Company'] = re.sub(r'[•Â$]', '', current_job_dict['Company']).strip()
                            company_found_index = i
                            break

                    start_desc_index = company_found_index + 1 if company_found_index != -1 else 0
                    
                    full_pos_desc_text = " ".join(lines_in_block[start_desc_index:]).strip()
                    full_pos_desc_text = re.sub(r'\n+', ' ', full_pos_desc_text)
                    full_pos_desc_text = re.sub(r'\s+', ' ', full_pos_desc_text)
                    full_pos_desc_text = re.sub(r'[•Â$]', '', full_pos_desc_text).strip()
                    
                    current_job_dict['Position'] = full_pos_desc_text if full_pos_desc_text else 'N/A'
                    
                    if current_job_dict['Company'] == 'N/A' and lines_in_block:
                        first_significant_line = lines_in_block[0]
                        if len(first_significant_line.split()) < 7 and re.match(r'^[A-Z][a-zA-Z\s.-]+$', first_significant_line):
                            current_job_dict['Company'] = re.sub(r'(?: - City, State| City, State)?', '', first_significant_line).strip()
                            current_job_dict['Company'] = re.sub(r'[•Â$]', '', current_job_dict['Company']).strip()
                            current_job_dict['Position'] = " ".join(lines_in_block[1:]).strip()
                            current_job_dict['Position'] = re.sub(r'\n+', ' ', current_job_dict['Position'])
                            current_job_dict['Position'] = re.sub(r'\s+', ' ', current_job_dict['Position'])
                            current_job_dict['Position'] = re.sub(r'[•Â$]', '', current_job_dict['Position']).strip()
                        else:
                            current_job_dict['Position'] = first_significant_line
                            current_job_dict['Position'] += " " + " ".join(lines_in_block[1:]).strip()
                            current_job_dict['Position'] = re.sub(r'\n+', ' ', current_job_dict['Position'])
                            current_job_dict['Position'] = re.sub(r'\s+', ' ', current_job_dict['Position'])
                            current_job_dict['Position'] = re.sub(r'[•Â$]', '', current_job_dict['Position']).strip()

                final_job_entries.append(current_job_dict)

        #Cari education
        education_pattern = r'Education(?:\s+and\s+Training)?\s*\n+(.*?)(?=\n\s*Skills|\n\s*Certifications|\n\s*Interests|\n\s*Additional Information|\Z)'
        education_match = re.search(education_pattern, text, re.DOTALL | re.IGNORECASE)
        if education_match:
            education_text = education_match.group(1).strip()
            
            school_pattern = r'([A-Za-z\s.,-]+(?:College|University|School|Institution))\s*(?:$|[^\n]*(?:City,\s*State))?'
            school_match = re.search(school_pattern, education_text, re.IGNORECASE)
            
            degree_pattern = r'(?:(Associate|Bachelor|Master|PhD|RN Diploma|High School Diploma|Post Secondary Training Certificate|Diploma).*?:\s*)?([A-Za-z\s]+(?:\s*in\s*[A-Za-z\s]+)?(?:/\s*[A-Za-z\s]+)?(?:-\s*[A-Za-z\s]+)?)'
            degree_match = re.search(degree_pattern, education_text, re.IGNORECASE)
            
            year_pattern = r'\b(19|20)\d{2}\b'
            years = re.findall(year_pattern, education_text)
            
            education_clean = education_text
            education_clean = re.sub(r'\n+', ' ', education_clean)
            education_clean = re.sub(r'\s+', ' ', education_clean)
            education_clean = re.sub(r'[•Â$]', '', education_clean).strip()
            
            degree_str = None
            if degree_match:
                if degree_match.group(1): 
                    degree_str = f"{degree_match.group(1).strip()} in {degree_match.group(2).strip()}"
                else:
                    degree_str = degree_match.group(2).strip()
                degree_str = re.sub(r'^[•\W]+', '', degree_str).strip()
                degree_str = re.sub(r'[\W]+$', '', degree_str).strip()

            all_info['Education'] = {
                'Full_Text': education_clean,
                'School': school_match.group(1).strip() if school_match else None,
                'Degree': degree_str,
                'Years': ', '.join(sorted(list(set(years)))) if years else None
            }

        #Cari certifications / licenses
        certifications_pattern = r'Certifications(?:\s*\/|\s*and\s+)?(?:Licenses)?\s*\n+(.*?)(?=\n\s*[A-Z][a-z]+\s*\n|\Z)'
        certifications_match = re.search(certifications_pattern, text, re.DOTALL | re.IGNORECASE)
        if certifications_match:
            certifications_text = certifications_match.group(1).strip()
            certifications_text = re.sub(r'\n+', ' ', certifications_text)
            certifications_text = re.sub(r'\s+', ' ', certifications_text)
            certifications_text = re.sub(r'[•Â$]', '', certifications_text).strip()
            all_info['Certifications'] = certifications_text

        all_skill_parts = []

        if 'Skills' in all_info and all_info['Skills']:
            if not re.match(r'Skills Used|I enjoy|my best|working as a team|if needed', all_info['Skills'], re.IGNORECASE):
                all_skill_parts.append(all_info['Skills'])
        
        for job in final_job_entries:
            if job.get('Position') and job['Position'] != 'N/A':
                resp_keyword_match = re.search(r'(?:Responsibilities|Duties)\s*(.*)', job['Position'], re.DOTALL | re.IGNORECASE)
                if resp_keyword_match:
                    all_skill_parts.append(resp_keyword_match.group(1).strip())
                else:
                    all_skill_parts.append(job['Position'])

        if 'Certifications' in all_info and all_info['Certifications']:
            all_skill_parts.append(all_info['Certifications'])

        combined_skills_string = " ".join(all_skill_parts)
        combined_skills_string = re.sub(r'\s{2,}', ' ', combined_skills_string)
        combined_skills_string = re.sub(r'[•,;:\-]', ' ', combined_skills_string)
        combined_skills_string = re.sub(r'\s{2,}', ' ', combined_skills_string).strip()
        
        all_info['Consolidated_Skills'] = combined_skills_string

        # Format summary untuk CV
        result = "=" * 30 + "\n"
        result += f"                        CV Summary (REGEX) \n"
        result += "=" * 30 + "\n\n"
        
        if 'Job_Title' in all_info:
            result += "JOB TITLE:\n"
            result += f"  {all_info['Job_Title']}\n\n"
        
        if 'Consolidated_Skills' in all_info and all_info['Consolidated_Skills']:
            result += "SKILLS:\n"
            result += f"  {all_info['Consolidated_Skills']}\n\n"
        
        if 'Summary' in all_info:
            result += "SUMMARY:\n"
            result += f"  {all_info['Summary']}\n\n"
        
        if 'Highlights' in all_info:
            result += "HIGHLIGHTS:\n"
            result += f"  {all_info['Highlights']}\n\n"
        
        if 'Accomplishments' in all_info:
            result += "ACCOMPLISHMENTS:\n"
            result += f"  {all_info['Accomplishments']}\n\n"
        
        if final_job_entries:
            result += "WORK EXPERIENCE:\n"
            for i, entry in enumerate(final_job_entries):
                result += f"  Date     : {entry.get('Date', 'N/A')}\n"
                result += f"  Company  : {entry.get('Company', 'N/A')}\n"
                result += f"  Position : {entry.get('Position', 'N/A')}\n"
                if i < len(final_job_entries) - 1:
                    result += f"  {'.' * 50}\n"
            result += "\n"
        
        if 'Education' in all_info:
            result += "EDUCATION:\n"
            edu = all_info['Education']
            
            if edu['School']:
                result += f"  School   : {edu['School']}\n"
            if edu['Degree']:
                result += f"  Degree   : {edu['Degree']}\n"
            if edu['Years']:
                result += f"  Years    : {edu['Years']}\n"
            
            result += f"  Full Info: {edu['Full_Text']}\n\n"
        
        return result