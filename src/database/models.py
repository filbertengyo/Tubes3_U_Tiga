from dataclasses import dataclass
from typing import Optional

@dataclass
class ApplicantProfile:
    applicant_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    date_of_birth: Optional[str] = None  
    address: str = ""
    phone_number: str = ""

@dataclass
class ApplicationDetail:
    detail_id: Optional[int] = None
    applicant_id: int = None
    application_role: str = ""
    cv_path: str = ""
