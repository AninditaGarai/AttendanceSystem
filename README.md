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

#### System Requirements
- Python 3.8 or higher
- A working webcam (built-in or external)
- Windows, macOS, or Linux operating system
- Minimum 4GB RAM
- 500MB free disk space

#### Software Dependencies
- CMake (required for face_recognition installation)
- dlib (required for face_recognition)
- Visual Studio Build Tools (Windows only, for C++ compilation)

#### Hardware Requirements
- Webcam with 640x480 resolution or higher
- Adequate lighting for face detection
- Stable internet connection (for initial package installation)

### Install Dependencies

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

### Note on face_recognition

The `face_recognition` package requires CMake and dlib to be installed on your system. If you encounter installation issues, please refer to the [face_recognition documentation](https://github.com/ageitgey/face_recognition).

### Environment Variables

This project does not require any environment variables to be set. All configuration is handled through the code and database files. The application uses default settings for:
- Database location: `data/attendance_system.db` (relative to project root)
- Face images location: `registered_faces/` (relative to project root)
- Camera resolution: 640x480 pixels
- Face recognition tolerance: 0.5

If you need to customize these settings, you can modify the constants in the respective Python files.


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

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with both CLI and GUI modes
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Code Style

- Follow PEP 8 guidelines for Python code
- Add docstrings to new functions
- Write clear, descriptive commit messages
- Keep functions small and focused
- Add comments for complex logic

### Testing

- Test face detection with different lighting conditions
- Verify student registration works correctly
- Check attendance tracking accuracy
- Test both CLI and GUI interfaces
- Ensure database operations work properly

## Developer Notes

### System Configuration
- The database is automatically created in the `data/` directory on first run
- Face images are stored in `registered_faces/` directory
- The system uses SQLite for data persistence
- Face recognition requires the `face_recognition` package
- Camera resolution is set to 640x480 for optimal performance
- Attendance is marked once per student per day

### Maintenance

#### Database Backup
To backup the database, copy the `data/attendance_system.db` file to a secure location.

#### Face Image Management
- Registered face images are stored as JPG files
- Images are named using the student's name (spaces replaced with underscores)
- To remove a student, delete their image file and use the delete function in the GUI

#### Performance Optimization
- The system processes frames at approximately 15 FPS in GUI mode
- Face recognition is performed every 5 frames to reduce CPU usage
- Camera resolution can be adjusted in the `open_camera()` function
- Face recognition tolerance can be modified in the attendance logic

#### Known Limitations
- Face recognition accuracy depends on lighting conditions
- Multiple faces in frame may cause recognition errors
- System requires a working webcam for operation
- Face recognition requires significant CPU resources
- Database is not encrypted - consider encryption for production use

## Troubleshooting

### Common Issues

**Issue: Camera not opening**
- Ensure your webcam is properly connected and not in use by another application
- Check camera permissions in your system settings
- Try running with administrator privileges

**Issue: face_recognition installation fails**
- Install CMake and Visual Studio Build Tools (Windows)
- Ensure you have a C++ compiler installed
- Refer to the [face_recognition documentation](https://github.com/ageitgey/face_recognition) for detailed installation instructions

**Issue: Face not detected**
- Ensure adequate lighting in the room
- Position yourself at an appropriate distance from the camera (2-3 feet)
- Make sure your face is clearly visible and not obscured

**Issue: Database errors**
- Ensure the `data/` directory exists and has write permissions
- Delete the database file and restart the application to recreate it
- Check that SQLite is properly installed

**Issue: GUI not responding**
- Close and restart the application
- Ensure you have enough system resources (RAM, CPU)
- Try using the CLI mode instead

