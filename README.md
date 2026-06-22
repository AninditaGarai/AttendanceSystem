# Face Attendance System

A beginner-friendly face attendance project using Python, OpenCV, face recognition, and SQLite. This system provides both CLI and GUI interfaces for registering students, tracking attendance using facial recognition, and managing attendance records. Designed for educational institutions and organizations seeking an automated attendance solution.

## Features

- Face detection using OpenCV Haar cascades
- Face recognition using the face_recognition library
- Student registration with face encoding
- Attendance tracking with timestamps
- CLI and GUI interfaces
- Export attendance data to CSV
- SQLite database for data persistence

## Project Architecture

The system follows a modular architecture with three main components:

### Database Layer (`database.py`)
- Handles all SQLite database operations
- Manages student and attendance tables
- Provides CRUD operations for student data
- Ensures data persistence and integrity

### Core Logic (`main.py`)
- Implements face detection and recognition algorithms
- Manages webcam interactions
- Handles student registration workflow
- Provides CLI-based user interface
- Coordinates between database and face recognition

### User Interface (`gui.py`)
- Tkinter-based graphical interface
- Real-time camera feed display
- Student registration and management
- Attendance tracking dashboard
- CSV export functionality

### Data Flow
1. Camera captures video frames
2. Face detection identifies faces in frames
3. Face recognition matches faces to registered students
4. Attendance is recorded in database
5. Results are displayed in CLI or GUI

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
├── database.py              # SQLite database operations and data access layer
├── gui.py                   # Tkinter GUI interface for visual interaction
├── main.py                  # CLI interface and core face recognition logic
├── requirements.txt         # Python package dependencies
├── data/                    # Database directory (auto-created on first run)
│   └── attendance_system.db # SQLite database file
├── registered_faces/        # Directory for storing registered face images
│   ├── Anindita.jpg         # Example registered face image
│   └── Shravya.jpg          # Example registered face image
└── .gitignore               # Git ignore patterns for Python projects
```

### File Descriptions

- **database.py**: Contains all database-related functions including table creation, student CRUD operations, and attendance tracking
- **gui.py**: Implements the Tkinter-based graphical user interface with real-time camera feed and attendance dashboard
- **main.py**: Provides command-line interface, face detection, recognition algorithms, and student registration workflow
- **requirements.txt**: Lists all Python dependencies required to run the application
- **data/**: Automatically created directory containing the SQLite database file
- **registered_faces/**: Stores JPG images of registered students for face recognition
- **.gitignore**: Specifies files and directories to exclude from Git version control

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

## Developer Notes

- The database is automatically created in the `data/` directory on first run
- Face images are stored in `registered_faces/` directory
- The system uses SQLite for data persistence
- Face recognition requires the `face_recognition` package
- Camera resolution is set to 640x480 for optimal performance
- Attendance is marked once per student per day

