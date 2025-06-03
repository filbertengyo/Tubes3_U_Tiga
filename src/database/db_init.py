import mysql

def get_connection():
    """Mengembalikan koneksi ke database MySQL."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ats_db"
    )

def init_db():
    """Membuat tabel ApplicantProfile dan ApplicationDetail jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(50),
        address TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT,
        cv_path TEXT,
        applied_position VARCHAR(255),
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(id)
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
