
# 🔐 Intrusion Detection and Lock System

This project is a **Python-based Intrusion Detection System** that captures an image of any unauthorized user, locks the system remotely, and alerts the owner via email. It integrates **OpenCV**, **Firebase Realtime Database**, **PyQt5**, and **SMTP** for a complete intrusion detection and response workflow.

---

## 🚀 Features

- 📸 **Intruder Capture** — Captures an image automatically using the system webcam.
- 🔒 **System Lock** — Locks the system screen with a secure password.
- ☁️ **Firebase Integration** — Syncs lock status and commands in real time.
- 📧 **Email Alerts** — Sends an email notification with the intruder's image.
- 🧱 **Task Manager & Hotkey Protection** — Disables Windows shortcuts and Task Manager to prevent forced exits.
- 🧩 **GUI Lock Screen** — Displays a fullscreen PyQt5-based password screen.

---

## 🧠 Components Overview

### 1. `capture.py`
Captures an image using the webcam when an intrusion is detected.


### 2. `firedb_listener.py`

Listens to Firebase Realtime Database for remote lock commands.
When `lock_command = True`, the system:

* Locks the screen
* Disables Task Manager and Win+Tab shortcuts
* Displays a fullscreen GUI that requires a password to unlock.

Uses:

* **PyQt5** for GUI
* **firebase_admin** for database listening
* **keyboard**, **win32api**, and **ctypes** for system-level control

---

### 3. `send_email.py`

Sends an **email alert** with the intruder’s image when a photo is captured.

* Uses **SMTP (Gmail)** for email delivery
* Attaches the captured image
* Includes a clickable “Lock & Blur Screen” button (via Google Apps Script)
* Deletes the image locally after successful send

---

### 4. `.bat` Files

Automate the execution of different scripts:

* `run_capture.bat` → Runs the camera capture script
* `run_firedb.bat` → Starts Firebase listener service
* `run_email.bat` → Sends pending intrusion alerts

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/balaprabhas/intrusion-detection.git
cd intrusion-detection
```

### 2️⃣ Install Dependencies

```bash
pip install opencv-python pyqt5 firebase-admin keyboard pywin32
```

### 3️⃣ Firebase Setup

* Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/).
* Enable **Realtime Database**.
* Generate a **Service Account Key** and place it in your project directory (DO NOT upload it to GitHub).
* Add the path in your code:

  ```python
  cred = credentials.Certificate("path_to_your_service_account.json")
  ```

### 4️⃣ Run the System

```bash
python firedb_listener.py
```

The script continuously monitors Firebase for a remote lock command.

---

## 🔒 Security Notes

* ⚠️ **Never commit your Firebase JSON key or passwords** to GitHub.
* Add this line to `.gitignore`:

  ```
  intruderlocksystem-firebase-adminsdk-*.json
  ```
* Regenerate your Firebase key if it was ever pushed to GitHub.

---

## 🧩 Folder Structure

```
intrusion_detection/
│
├── capture.py
├── firedb_listener.py
├── send_email.py
├── run_capture.bat
├── run_email.bat
├── run_firedb.bat
├── unsent_photos/
│   └── (Captured images)
├── .gitignore
└── README.md
```

---

## 🧠 Future Improvements

* 🌐 Web Dashboard to monitor intrusion activity
* 🔊 Sound alert on detection
* ☁️ Integration with cloud storage (Google Drive / AWS S3)
* 🤖 AI-based face recognition for known users

---




