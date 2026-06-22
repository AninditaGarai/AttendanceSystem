import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "attendance_system.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            face_encoding TEXT,
            image_path TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id),
            UNIQUE(student_id, date)
        )
        """
    )

    cursor.execute("PRAGMA table_info(students)")
    student_columns = [column[1] for column in cursor.fetchall()]

    if "student_code" not in student_columns:
        cursor.execute("ALTER TABLE students ADD COLUMN student_code TEXT")

    connection.commit()
    connection.close()


def add_student(name, image_path, face_encoding=None, student_code=None):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, face_encoding, image_path, created_at, student_code)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                face_encoding,
                image_path,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                student_code,
            ),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def update_student_encoding(student_id, face_encoding):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE students
        SET face_encoding = ?
        WHERE id = ?
        """,
        (face_encoding, student_id),
    )

    connection.commit()
    connection.close()


def get_all_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, image_path, created_at, student_code
        FROM students
        ORDER BY id
        """
    )
    students = cursor.fetchall()
    connection.close()
    return students


def get_students_for_recognition():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, face_encoding, image_path
        FROM students
        ORDER BY id
        """
    )
    students = cursor.fetchall()
    connection.close()
    return students


def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    connection.commit()
    connection.close()


def mark_attendance(student_id, name):
    now = datetime.now()
    attendance_date = now.strftime("%Y-%m-%d")
    attendance_time = now.strftime("%H:%M:%S")
    created_at = now.strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO attendance (student_id, name, date, time, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (student_id, name, attendance_date, attendance_time, created_at),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def get_today_attendance():
    today = datetime.now().strftime("%Y-%m-%d")
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(students.student_code, ''), attendance.name, attendance.date, attendance.time
        FROM attendance
        LEFT JOIN students ON students.id = attendance.student_id
        WHERE attendance.date = ?
        ORDER BY attendance.time DESC
        """,
        (today,),
    )
    records = cursor.fetchall()
    connection.close()
    return records


def show_database_location():
    print(f"Database ready at: {DATABASE_PATH}")

