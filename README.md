# Face Attendance System

A beginner-friendly face attendance project using Python, OpenCV, face recognition, and SQLite.

## Installation

### Prerequisites

- Python 3.8 or higher
- A working webcam
- Windows, macOS, or Linux

### Install Dependencies

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

### Note on face_recognition

The `face_recognition` package requires CMake and dlib to be installed on your system. If you encounter installation issues, please refer to the [face_recognition documentation](https://github.com/ageitgey/face_recognition).


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

## Usage Examples

### CLI Mode

1. Run `python main.py` to start the CLI interface
2. Select option 1 to register a new person
3. Select option 2 to start attendance mode
4. Select option 3 to view registered people
5. Select option 4 to test face detection
6. Select option 5 to exit

### GUI Mode

Run `python gui.py` to launch the graphical interface with features for:
- Student registration
- Live attendance tracking
- Attendance export to CSV
- Student management


## Contributing

Contributions are welcome! Please follow these guidelines:

- Fork the repository
- Create a feature branch
- Make your changes
- Test thoroughly
- Submit a pull request

