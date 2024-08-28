from flask import Flask, request, jsonify
import time
import ssl
import re
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Dictionary to store last ping time of each host
host_status = {}

# Secure API key
SECURE_API_KEY = "your-secure-api-key"

# Regex to validate hostname
hostname_regex = re.compile(r"^[a-zA-Z0-9-]{1,63}$")

# Alert settings
ALERT_THRESHOLD = 600  # 10 minutes in seconds
ALERT_EMAILS = ["admin@example.com"]  # List of email addresses to alert
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@example.com"
SMTP_PASSWORD = "your-email-password"

def send_email_alert(hostname):
    subject = f"ALERT: Host {hostname} missed a ping!"
    body = f"Host {hostname} has not pinged within the last {ALERT_THRESHOLD / 60} minutes."
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = ", ".join(ALERT_EMAILS)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, ALERT_EMAILS, text)
        server.quit()
        print(f"Alert email sent for {hostname}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")

def monitor_hosts():
    while True:
        current_time = time.time()
        for hostname, last_ping in list(host_status.items()):
            if current_time - last_ping > ALERT_THRESHOLD:
                send_email_alert(hostname)
                del host_status[hostname]  # Remove the host to avoid duplicate alerts
        time.sleep(60)  # Check every minute

@app.route("/ping", methods=["POST"])
def ping():
    auth_header = request.headers.get('Authorization')
    if auth_header != f'Bearer {SECURE_API_KEY}':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    hostname = data.get('hostname')
    
    if not hostname_regex.match(hostname):
        return jsonify({"error": "Invalid hostname"}), 400

    host_status[hostname] = time.time()
    return jsonify({"message": "Ping received"}), 200

@app.route("/status", methods=["GET"])
def status():
    return jsonify(host_status), 200

if __name__ == "__main__":
    # Start the host monitor in a separate thread
    monitor_thread = threading.Thread(target=monitor_hosts, daemon=True)
    monitor_thread.start()
    
    # Start the Flask app with SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('path/to/cert.pem', 'path/to/key.pem')
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
