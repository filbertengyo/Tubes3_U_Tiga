from dataclasses import dataclass

@dataclass
class ApplicantProfile:
    id: int = None
    name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""

@dataclass
class ApplicationDetail:
    id: int = None
    applicant_id: int = None
    cv_path: str = ""
    applied_position: str = ""
