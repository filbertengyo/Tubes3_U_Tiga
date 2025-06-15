import pymysql

def get_connection():
    """Mengembalikan koneksi ke database MySQL menggunakan PyMySQL."""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ats_db",
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False
    )

def init_db():
    """Membuat tabel ApplicantProfile dan ApplicationDetail jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        applicant_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) DEFAULT NULL,
        last_name VARCHAR(50) DEFAULT NULL,
        date_of_birth DATE DEFAULT NULL,
        address VARCHAR(255) DEFAULT NULL,
        phone_number VARCHAR(20) DEFAULT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        detail_id INT AUTO_INCREMENT PRIMARY KEY,
        applicant_id INT NOT NULL,
        application_role VARCHAR(100) DEFAULT NULL,
        cv_path TEXT,
        FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
