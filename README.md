# Face Attendance System

A beginner-friendly face attendance project using Python, OpenCV, face recognition, and SQLite.

## Installation

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

## Project Structure

```
AttendanceSystem/
├── database.py              # SQLite database operations
├── gui.py                   # Tkinter GUI interface
├── main.py                  # CLI interface and face recognition logic
├── requirements.txt         # Python dependencies
├── data/                    # Database directory
│   └── attendance_system.db
└── registered_faces/        # Stored face images
```

## Current Module

Module A: Open laptop webcam and show live video feed.

## API Documentation

### Database Functions

- `create_tables()` - Initialize database tables
- `add_student(name, image_path, face_encoding, student_code)` - Register a new student
- `get_all_students()` - Retrieve all registered students
- `mark_attendance(student_id, name)` - Mark attendance for a student
- `get_today_attendance()` - Get today's attendance records

### Main Functions

- `detect_faces_webcam()` - Open webcam and detect faces
- `register_new_person()` - Register a new person with face encoding
- `start_attendance()` - Start attendance recognition mode
- `show_menu()` - Display CLI menu interface

## Run

```powershell
python main.py
```
