from .db_init import get_connection
from .models import ApplicantProfile, ApplicationDetail

def insert_applicant(profile: ApplicantProfile) -> int:
    """Menyimpan profil applicant, return id yang di-generate."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
        VALUES (%s, %s, %s, %s, %s)
    """, (profile.first_name, profile.last_name, profile.date_of_birth, profile.address, profile.phone_number))

    applicant_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return applicant_id

def insert_application(detail: ApplicationDetail) -> int:
    """Menyimpan detail lamaran dan path CV."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
        VALUES (%s, %s, %s)
    """, (detail.applicant_id, detail.application_role, detail.cv_path))

    detail_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return detail_id

def get_all_applications() -> list[tuple]:
    """Mengambil semua aplikasi dan CV path-nya."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ap.applicant_id, ap.first_name, ap.last_name, ap.date_of_birth, ap.address, ap.phone_number, ad.cv_path, ad.application_role
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
