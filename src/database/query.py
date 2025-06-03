from .db_init import get_connection
from .models import ApplicantProfile, ApplicationDetail

def insert_applicant(profile: ApplicantProfile) -> int:
    """Menyimpan profil applicant, return id yang di-generate."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ApplicantProfile (name, email, phone, address)
        VALUES (%s, %s, %s, %s)
    """, (profile.name, profile.email, profile.phone, profile.address))

    conn.commit()
    inserted_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return inserted_id

def insert_application(detail: ApplicationDetail) -> int:
    """Menyimpan detail lamaran dan path CV."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ApplicationDetail (applicant_id, cv_path, applied_position)
        VALUES (%s, %s, %s)
    """, (detail.applicant_id, detail.cv_path, detail.applied_position))

    conn.commit()
    inserted_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return inserted_id

def get_all_applications() -> list[tuple]:
    """Mengambil semua aplikasi dan CV path-nya."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ap.id, ap.name, ap.email, ap.phone, ap.address, ad.cv_path, ad.applied_position
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.id = ad.applicant_id
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
