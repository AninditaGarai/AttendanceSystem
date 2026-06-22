import cv2
import json
import numpy as np
from pathlib import Path

from database import (
    add_student,
    create_tables,
    get_all_students,
    get_students_for_recognition,
    mark_attendance,
    show_database_location,
    update_student_encoding,
)


BASE_DIR = Path(__file__).resolve().parent
REGISTERED_FACES_DIR = BASE_DIR / "registered_faces"


def get_face_recognition_library():
    try:
        import face_recognition

        return face_recognition
    except ModuleNotFoundError:
        print("face_recognition is not installed yet.")
        print("Recognition needs this package. Detection can work without it.")
        return None


def open_camera():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera


def is_exit_key(key):
    """Check if the key is an exit key (q, Q, or Esc)."""
    return key in (ord("q"), ord("Q"), 27)


def detect_faces_webcam():
    camera = open_camera()
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened successfully.")
    print("Face detection started.")
    print("Press Q to close the webcam window.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read frame from webcam.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80),
        )

        for x, y, width, height in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2,
            )

        cv2.imshow("Face Attendance System - Face Detection", frame)

        key = cv2.waitKey(10) & 0xFF

        if is_exit_key(key):
            break

    camera.release()
    cv2.destroyAllWindows()


def register_new_person():
    face_recognition = get_face_recognition_library()

    if face_recognition is None:
        print("Install face_recognition before registering faces for recognition.")
        return

    name = input("Enter the person's name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    safe_name = name.replace(" ", "_")
    REGISTERED_FACES_DIR.mkdir(exist_ok=True)

    camera = open_camera()
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Registration started.")
    print("Keep only one face in the camera.")
    print("Press C to capture your face.")
    print("Press Q to cancel registration.")
    status_message = "Press C to capture, Q to cancel"

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read frame from webcam.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80),
        )

        for x, y, width, height in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2,
            )

        cv2.putText(
            frame,
            status_message,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        cv2.imshow("Register New Person", frame)
        key = cv2.waitKey(1) & 0xFF

        if is_exit_key(key):
            print("Registration cancelled.")
            break

        if key in (ord("c"), ord("C")):
            if len(faces) == 0:
                status_message = "No face detected. Move closer and try again."
                print(status_message)
                continue

            if len(faces) > 1:
                status_message = "More than one face detected. Keep only one person."
                print(status_message)
                continue

            image_path = REGISTERED_FACES_DIR / f"{safe_name}.jpg"
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_frame)

            if len(encodings) != 1:
                status_message = "Could not encode face. Try better lighting."
                print(status_message)
                continue

            face_encoding = json.dumps(encodings[0].tolist())
            saved_to_database = add_student(
                name=name,
                image_path=str(image_path),
                face_encoding=face_encoding,
            )

            if not saved_to_database:
                status_message = f"{name} is already registered."
                print(f"{name} is already registered. Please use another name.")
                cv2.putText(
                    frame,
                    status_message,
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
                cv2.imshow("Register New Person", frame)
                cv2.waitKey(1500)
                break

            cv2.imwrite(str(image_path), frame)
            status_message = f"{name} registered successfully."
            print(status_message)
            print(f"Face image saved at: {image_path}")
            cv2.putText(
                frame,
                status_message,
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Register New Person", frame)
            cv2.waitKey(1500)
            break

    camera.release()
    cv2.destroyAllWindows()


def start_attendance():
    face_recognition = get_face_recognition_library()

    if face_recognition is None:
        print("Install face_recognition before starting attendance.")
        return

    known_students = load_known_students(face_recognition)

    if not known_students:
        print("No registered face encodings found.")
        print("Register a person first after face_recognition is installed.")
        return

    known_ids = [student["id"] for student in known_students]
    known_names = [student["name"] for student in known_students]
    known_encodings = [student["encoding"] for student in known_students]

    camera = open_camera()

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Attendance started.")
    print("Press Q to close attendance mode.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read frame from webcam.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            face_locations,
        )

        for face_location, face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(
                known_encodings,
                face_encoding,
                tolerance=0.5,
            )
            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding,
            )

            name = "Unknown"
            box_color = (0, 0, 255)

            if len(face_distances) > 0:
                best_match_index = int(np.argmin(face_distances))

                if matches[best_match_index]:
                    student_id = known_ids[best_match_index]
                    name = known_names[best_match_index]
                    was_marked = mark_attendance(student_id, name)
                    box_color = (0, 255, 0)

                    if was_marked:
                        label = f"{name} - Present"
                    else:
                        label = f"{name} - Already marked"
                else:
                    label = name
            else:
                label = name

            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                box_color,
                2,
            )

        cv2.putText(
            frame,
            "Press Q or Esc to close",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )
        cv2.imshow("Face Attendance System - Attendance", frame)
        key = cv2.waitKey(10) & 0xFF

        if is_exit_key(key):
            break

    camera.release()
    cv2.destroyAllWindows()


def load_known_students(face_recognition):
    known_students = []
    students = get_students_for_recognition()

    for student_id, name, face_encoding_text, image_path in students:
        if face_encoding_text:
            known_students.append(
                {
                    "id": student_id,
                    "name": name,
                    "encoding": np.array(json.loads(face_encoding_text)),
                }
            )
            continue

        image_file = Path(image_path)

        if not image_file.exists():
            print(f"Image missing for {name}: {image_path}")
            continue

        image = face_recognition.load_image_file(str(image_file))
        encodings = face_recognition.face_encodings(image)

        if len(encodings) != 1:
            print(f"Could not create encoding for {name}. Re-register this person.")
            continue

        face_encoding_text = json.dumps(encodings[0].tolist())
        update_student_encoding(student_id, face_encoding_text)
        known_students.append(
            {
                "id": student_id,
                "name": name,
                "encoding": encodings[0],
            }
        )

    return known_students


def show_menu():
    while True:
        print("\n===== Face Attendance System =====")
        print("1. Register New Person")
        print("2. Start Attendance")
        print("3. Show Registered People")
        print("4. Test Face Detection")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_new_person()
        elif choice == "2":
            start_attendance()
        elif choice == "3":
            show_registered_people()
        elif choice == "4":
            detect_faces_webcam()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


def show_registered_people():
    students = get_all_students()

    if not students:
        print("No people registered yet.")
        return

    print("\nRegistered people:")
    for student_id, name, image_path, created_at, student_code in students:
        code_text = student_code or "No code"
        print(f"{student_id}. {code_text} | {name} | {created_at} | {image_path}")


if __name__ == "__main__":
    create_tables()
    show_database_location()
    show_menu()
