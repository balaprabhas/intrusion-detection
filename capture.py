import cv2
import os
from datetime import datetime

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        filename = datetime.now().strftime("intruder_%Y%m%d_%H%M%S.jpg")
        filepath = os.path.join("unsent_photos", filename)
        os.makedirs("unsent_photos", exist_ok=True)
        cv2.imwrite(filepath, frame)
        cap.release()
        return filepath
    cap.release()
    return None


capture_image()
