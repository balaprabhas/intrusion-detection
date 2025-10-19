import os
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import firebase_admin
from firebase_admin import credentials, db
from email.utils import make_msgid, formatdate


# --- Firebase Admin Init ---
cred = credentials.Certificate("intruderlocksystem-firebase-adminsdk-fbsvc-269313203c.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://intruderlocksystem-default-rtdb.firebaseio.com/"
})
script_url="https://script.google.com/macros/s/AKfycbwbRsyC-o9voRofO4XfD14AMZpTLulW78O-mE18a0P6PRtLAFAhEvEQPtojNnoo5a_w/exec"
password = 'arya29!!'

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def send_intruder_email(photo_path, receiver_email):
    sender_email = "maskuaravind1234@gmail.com"
    sender_password = "srliwnxxwaydcpfc"
    subject = "🚨 Intruder Alert!"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align:center;">
        <h2 style="color:red;">🚨 Intruder Detected!</h2>
        <p>Password to unlock: <b>{password}</b></p>
        <p>Someone tried to access your device. Below is the captured photo:</p>
        <img src="cid:intruder" width="300" style="border:2px solid #555;"/><br><br>
        <a href="{script_url}" 
        style="padding:12px 20px; background-color:#d9534f; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">
        🔒 Lock & Blur Screen Now</a>
        <p>If this was you, ignore this message. Otherwise, your screen will lock automatically.</p>
    </body>
    </html>
    """

    text_content = "INTRUDER ALERT!\nSomeone tried to access your device.\n"

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Reply-To"] = sender_email
    msg["Message-ID"] = make_msgid()
    msg["Date"] = formatdate(localtime=True)


    alt = MIMEMultipart("alternative")
    msg.attach(alt)
    alt.attach(MIMEText(text_content, "plain"))
    alt.attach(MIMEText(html_content, "html"))

    with open(photo_path, "rb") as f:
        img = MIMEImage(f.read(), _subtype="jpeg")
        img.add_header("Content-ID", "<intruder>")
        img.add_header("Content-Disposition", "inline", filename="intruder.jpg")
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("✅ Email sent successfully!")
    os.remove(photo_path)

UPLOAD_FOLDER = "unsent_photos"  # folder where images are stored

if is_connected():
    photos = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)
              if f.lower().endswith((".jpg", ".jpeg", ".png"))]  # only image files
    
    if photos:  # if there are images in the folder
        for photo in photos:
            send_intruder_email(photo, "maskuaravind29@gmail.com")
        print("✅ Email sent successfully!")
    else:
        print("No photos found in upload_photos folder.")
    
       
else:
    print("📴 No Internet. Email not sent.")