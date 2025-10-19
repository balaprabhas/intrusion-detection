import sys
import time
import threading
import ctypes
import firebase_admin
from firebase_admin import credentials, db
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import win32con
import win32gui
import winreg
import keyboard
import os

def resource_path(rel_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

SERVICE_JSON = "intruderlocksystem-firebase-adminsdk-fbsvc-269313203c.json"
cred_path = resource_path(SERVICE_JSON)
# === Firebase Init ===
cred = credentials.Certificate(cred_path)
#cred = credentials.Certificate("intruderlocksystem-firebase-adminsdk-fbsvc-269313203c.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://intruderlocksystem-default-rtdb.firebaseio.com/"
})
ref = db.reference("lock_command")

# === Constants ===
CORRECT_PASSWORD = "arya29!!"

# === Helper Functions ===
def block_input(state=True):
    ctypes.windll.user32.BlockInput(state)

def hide_taskbar():
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

def show_taskbar():
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

def disable_task_manager():
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
    winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)

def enable_task_manager():
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
    winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)



def block_win_tab():
    keyboard.block_key('windows')
    keyboard.add_hotkey('windows+tab', lambda: None, suppress=True) 
    
# === Lock Screen GUI ===
class LockScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | Qt.Tool)
        self.showFullScreen()
        self.setStyleSheet("background-color: black; color: white; font-size: 24px;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("🔒 System Locked\n\nEnter Password to Unlock:")
        label.setAlignment(Qt.AlignCenter)

        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)
        self.input.setFixedWidth(300)
        self.input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 20px;
                border: 2px solid white;
                border-radius: 8px;
                background-color: #222;
                color: white;
            }
        """)

        btn = QPushButton("Unlock")
        btn.setFixedWidth(150)
        btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 18px;
                background-color: #00aa00;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
        """)

        self.msg = QLabel("")
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setStyleSheet("font-size: 20px; color: red;")

        layout.addWidget(label)
        layout.addSpacing(20)
        layout.addWidget(self.input, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.msg)

        self.setLayout(layout)

        btn.clicked.connect(self.check_unlock)


    def check_unlock(self):
        entered = self.input.text()
        if entered == CORRECT_PASSWORD:
            ref.set({"lock_command": False, "lock_password": CORRECT_PASSWORD})
            self.msg.setText("✅ Unlocked")
            block_input(False)
            enable_task_manager()
            show_taskbar()
            keyboard.unblock_key('windows')
            keyboard.remove_hotkey('windows+tab')

            QApplication.quit()
        else:
            self.msg.setText("❌ Incorrect password")

# === Trigger GUI ===
def show_kiosk_lock():
    def run():        
        hide_taskbar()
        disable_task_manager()
        block_win_tab()
        app = QApplication(sys.argv)
        window = LockScreen()
        window.show()
        app.exec_()
    threading.Thread(target=run).start()

# === Firebase Polling ===
def listen_lock_command():
    last_state = None
    while True:
        data = ref.get()
        if isinstance(data, dict) and data.get("lock_command") == True and data != last_state:
            print("🔐 Lock triggered!")
            show_kiosk_lock()
        last_state = data
        time.sleep(2)

# === Start Listening ===
print("🔁 Waiting for lock command...")
listen_lock_command()