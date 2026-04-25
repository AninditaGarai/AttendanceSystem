import csv
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

from database import (
    add_student,
    create_tables,
    delete_student,
    get_all_students,
    get_today_attendance,
    mark_attendance,
)
from main import (
    REGISTERED_FACES_DIR,
    get_face_recognition_library,
    load_known_students,
    open_camera,
)


class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Attendance System")
        self.root.geometry("1420x780")
        self.root.minsize(1180, 680)
        self.root.configure(bg="#eef3f8")

        create_tables()
        self.face_recognition = get_face_recognition_library()
        self.camera = None
        self.current_frame = None
        self.mode = "idle"
        self.known_students = []
        self.known_ids = []
        self.known_names = []
        self.known_encodings = []
        self.last_labels = []
        self.frame_count = 0
        self.status_var = tk.StringVar(value="Ready")
        self.stats_var = tk.StringVar(value="")

        self.setup_styles()
        self.build_layout()
        self.refresh_tables()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10), background="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e5e7eb")
        style.configure("Sidebar.TButton", font=("Segoe UI", 10, "bold"), padding=12)
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), padding=10)

    def build_layout(self):
        sidebar = tk.Frame(self.root, bg="#102235", width=168)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Attendance\nSystem",
            bg="#102235",
            fg="#ffffff",
            font=("Segoe UI", 19, "bold"),
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=22, pady=(30, 28))

        ttk.Button(sidebar, text="Take Attendance", style="Sidebar.TButton", command=self.start_attendance).pack(
            fill="x", padx=16, pady=7
        )
        ttk.Button(sidebar, text="Stop Camera", style="Sidebar.TButton", command=self.stop_camera).pack(
            fill="x", padx=16, pady=7
        )
        ttk.Button(sidebar, text="Export Excel", style="Sidebar.TButton", command=self.export_attendance).pack(
            fill="x", padx=16, pady=7
        )
        ttk.Button(sidebar, text="Refresh Tables", style="Sidebar.TButton", command=self.refresh_tables).pack(
            fill="x", padx=16, pady=7
        )

        tk.Label(
            sidebar,
            textvariable=self.stats_var,
            bg="#102235",
            fg="#d7e2ee",
            font=("Segoe UI", 10),
            justify="left",
            anchor="w",
        ).pack(side="bottom", fill="x", padx=22, pady=34)

        content = tk.Frame(self.root, bg="#eef3f8")
        content.pack(side="left", fill="both", expand=True)

        header = tk.Frame(content, bg="#ffffff")
        header.pack(fill="x", padx=16, pady=(16, 10))

        tk.Label(
            header,
            text="Live Face Attendance",
            bg="#ffffff",
            fg="#172033",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).pack(side="left", padx=20, pady=(16, 3))

        tk.Label(
            header,
            textvariable=self.status_var,
            bg="#eef5ff",
            fg="#244b7a",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=6,
        ).pack(side="right", padx=20, pady=16)

        body = tk.Frame(content, bg="#eef3f8")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        camera_outer = tk.Frame(body, bg="#ffffff")
        camera_outer.pack(side="left", fill="both", expand=True, padx=(0, 14))

        self.video_label = tk.Label(
            camera_outer,
            text="Camera preview",
            bg="#0f1c2d",
            fg="#dbeafe",
            font=("Segoe UI", 18, "bold"),
        )
        self.video_label.pack(fill="both", expand=True, padx=10, pady=10)

        right_panel = tk.Frame(body, bg="#ffffff", width=430)
        right_panel.pack(side="left", fill="y")
        right_panel.pack_propagate(False)

        self.build_registration_panel(right_panel)
        self.build_attendance_panel(right_panel)

    def build_registration_panel(self, parent):
        tk.Label(
            parent,
            text="Student Registration",
            bg="#ffffff",
            fg="#172033",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        ).pack(fill="x", padx=20, pady=(20, 12))

        form = tk.Frame(parent, bg="#ffffff")
        form.pack(fill="x", padx=20)

        tk.Label(form, text="Student Code", bg="#ffffff", fg="#374151", font=("Segoe UI", 10), width=13, anchor="w").grid(
            row=0, column=0, sticky="w", pady=6
        )
        self.code_entry = tk.Entry(form, font=("Segoe UI", 10), relief="solid", bd=1)
        self.code_entry.grid(row=0, column=1, sticky="ew", pady=6)

        tk.Label(form, text="Name", bg="#ffffff", fg="#374151", font=("Segoe UI", 10), width=13, anchor="w").grid(
            row=1, column=0, sticky="w", pady=6
        )
        self.name_entry = tk.Entry(form, font=("Segoe UI", 10), relief="solid", bd=1)
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=6)
        form.columnconfigure(1, weight=1)

        ttk.Button(parent, text="Start Registration", style="Action.TButton", command=self.start_registration).pack(
            fill="x", padx=20, pady=(14, 8)
        )
        self.capture_button = ttk.Button(
            parent,
            text="Capture Face",
            style="Action.TButton",
            command=self.capture_registration,
            state="disabled",
        )
        self.capture_button.pack(fill="x", padx=20, pady=(0, 16))

        tk.Label(
            parent,
            text="Student Management",
            bg="#ffffff",
            fg="#172033",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        ).pack(fill="x", padx=20, pady=(4, 10))

        ttk.Button(parent, text="Delete Student", style="Danger.TButton", command=self.delete_selected_student).pack(
            fill="x", padx=20, pady=(0, 14)
        )

        self.students_tree = ttk.Treeview(parent, columns=("ID", "Code", "Name"), show="headings", height=5)
        for column, width in (("ID", 45), ("Code", 120), ("Name", 190)):
            self.students_tree.heading(column, text=column)
            self.students_tree.column(column, width=width, anchor="w")
        self.students_tree.pack(fill="x", padx=20, pady=(0, 18))

    def build_attendance_panel(self, parent):
        tk.Label(
            parent,
            text="Today's Attendance",
            bg="#ffffff",
            fg="#172033",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        ).pack(fill="x", padx=20, pady=(2, 10))

        self.attendance_tree = ttk.Treeview(parent, columns=("Code", "Name", "Time"), show="headings", height=8)
        for column, width in (("Code", 125), ("Name", 175), ("Time", 85)):
            self.attendance_tree.heading(column, text=column)
            self.attendance_tree.column(column, width=width, anchor="w")
        self.attendance_tree.pack(fill="x", padx=20, pady=(0, 10))

        ttk.Button(
            parent,
            text="Delete Selected",
            style="Danger.TButton",
            command=self.delete_selected_student,
        ).pack(fill="x", padx=20, pady=(0, 16))

    def start_registration(self):
        if self.face_recognition is None:
            self.set_status("face_recognition missing")
            return

        if not self.name_entry.get().strip():
            self.set_status("Enter student name")
            return

        self.mode = "registration"
        self.capture_button.configure(state="normal")
        self.start_camera()
        self.set_status("Registration running")

    def capture_registration(self):
        if self.current_frame is None:
            self.set_status("Camera not ready")
            return

        name = self.name_entry.get().strip()
        student_code = self.code_entry.get().strip()

        if not name:
            self.set_status("Enter student name")
            return

        rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        face_locations = self.face_recognition.face_locations(rgb_frame)

        if len(face_locations) != 1:
            self.set_status("Keep exactly one face visible")
            return

        encodings = self.face_recognition.face_encodings(rgb_frame, face_locations)

        if len(encodings) != 1:
            self.set_status("Face encoding failed")
            return

        REGISTERED_FACES_DIR.mkdir(exist_ok=True)
        safe_name = name.replace(" ", "_")
        image_path = REGISTERED_FACES_DIR / f"{safe_name}.jpg"
        face_encoding = json.dumps(encodings[0].tolist())
        saved = add_student(
            name=name,
            image_path=str(image_path),
            face_encoding=face_encoding,
            student_code=student_code,
        )

        if not saved:
            self.set_status(f"{name} already registered")
            return

        cv2.imwrite(str(image_path), self.current_frame)
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.capture_button.configure(state="disabled")
        self.mode = "idle"
        self.load_known_faces()
        self.refresh_tables()
        self.set_status(f"Registered {name}")

    def start_attendance(self):
        if self.face_recognition is None:
            self.set_status("face_recognition missing")
            return

        self.load_known_faces()

        if not self.known_students:
            self.set_status("Register students first")
            return

        self.mode = "attendance"
        self.capture_button.configure(state="disabled")
        self.start_camera()
        self.set_status("Attendance running")

    def start_camera(self):
        if self.camera is None:
            self.camera = open_camera()

        if not self.camera.isOpened():
            self.camera = None
            self.set_status("Camera open failed")
            return

        self.update_camera()

    def stop_camera(self):
        self.mode = "idle"
        self.capture_button.configure(state="disabled")
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.video_label.configure(image="", text="Camera stopped")
        self.set_status("Camera stopped")

    def update_camera(self):
        if self.camera is None:
            return

        success, frame = self.camera.read()

        if not success:
            self.stop_camera()
            self.set_status("Could not read camera")
            return

        self.current_frame = frame.copy()
        display_frame = frame.copy()

        if self.mode == "registration":
            display_frame = self.draw_registration_frame(display_frame)
        elif self.mode == "attendance":
            display_frame = self.process_attendance_frame(display_frame)

        self.show_frame(display_frame)
        self.root.after(15, self.update_camera)

    def draw_registration_frame(self, frame):
        self.draw_banner(frame, "Registration running")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = self.face_recognition.face_locations(rgb_frame)

        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Ready", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return frame

    def process_attendance_frame(self, frame):
        self.draw_banner(frame, "Attendance running")
        self.frame_count += 1

        if self.frame_count % 5 != 0:
            self.draw_last_labels(frame)
            return frame

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = self.face_recognition.face_locations(rgb_small_frame)
        face_encodings = self.face_recognition.face_encodings(rgb_small_frame, face_locations)
        self.last_labels = []

        for face_location, face_encoding in zip(face_locations, face_encodings):
            distances = self.face_recognition.face_distance(self.known_encodings, face_encoding)
            label = "Unknown"
            color = (0, 0, 255)

            if len(distances) > 0:
                best_index = int(np.argmin(distances))
                matches = self.face_recognition.compare_faces(
                    self.known_encodings,
                    face_encoding,
                    tolerance=0.5,
                )

                if matches[best_index]:
                    student_id = self.known_ids[best_index]
                    name = self.known_names[best_index]
                    marked_now = mark_attendance(student_id, name)
                    color = (0, 180, 0)
                    label = name
                    if marked_now:
                        self.set_status(f"Marked {name} at {datetime.now().strftime('%H:%M:%S')}")
                    self.refresh_attendance_table()

            top, right, bottom, left = face_location
            self.last_labels.append(((top * 4, right * 4, bottom * 4, left * 4), label, color))

        self.draw_last_labels(frame)
        return frame

    def draw_banner(self, frame, text):
        cv2.rectangle(frame, (80, 45), (600, 90), (45, 29, 18), -1)
        cv2.putText(frame, text, (95, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    def draw_last_labels(self, frame):
        for (top, right, bottom, left), label, color in self.last_labels:
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    def show_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image.thumbnail((840, 620))
        photo = ImageTk.PhotoImage(image=image)
        self.video_label.configure(image=photo, text="")
        self.video_label.image = photo

    def load_known_faces(self):
        self.known_students = load_known_students(self.face_recognition)
        self.known_ids = [student["id"] for student in self.known_students]
        self.known_names = [student["name"] for student in self.known_students]
        self.known_encodings = [student["encoding"] for student in self.known_students]

    def refresh_tables(self):
        self.refresh_students_table()
        self.refresh_attendance_table()
        self.update_stats()

    def refresh_students_table(self):
        for row in self.students_tree.get_children():
            self.students_tree.delete(row)

        for student_id, name, _image_path, _created_at, student_code in get_all_students():
            self.students_tree.insert("", "end", values=(student_id, student_code or "", name))

    def refresh_attendance_table(self):
        for row in self.attendance_tree.get_children():
            self.attendance_tree.delete(row)

        for student_code, name, _date, time in get_today_attendance():
            self.attendance_tree.insert("", "end", values=(student_code, name, time))
        self.update_stats()

    def update_stats(self):
        students_count = len(get_all_students())
        attendance_count = len(get_today_attendance())
        self.stats_var.set(f"Students: {students_count}\nAttendance today: {attendance_count}")

    def delete_selected_student(self):
        selected = self.students_tree.selection()

        if not selected:
            messagebox.showinfo("Delete Student", "Select a student from the Registered People table.")
            return

        values = self.students_tree.item(selected[0], "values")
        student_id = int(values[0])
        name = values[2]

        if not messagebox.askyesno("Delete Student", f"Delete {name} and their attendance records?"):
            return

        delete_student(student_id)
        self.load_known_faces()
        self.refresh_tables()
        self.set_status(f"Deleted {name}")

    def export_attendance(self):
        records = get_today_attendance()

        if not records:
            messagebox.showinfo("Export Excel", "No attendance records to export today.")
            return

        default_name = f"attendance_{datetime.now().strftime('%Y-%m-%d')}.csv"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv")],
        )

        if not file_path:
            return

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Code", "Name", "Date", "Time"])
            writer.writerows(records)

        self.set_status("Attendance exported")

    def set_status(self, message):
        self.status_var.set(message)

    def close_app(self):
        if self.camera is not None:
            self.camera.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    FaceAttendanceApp(root)
    root.mainloop()
