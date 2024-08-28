import requests
import time
import socket

# Configuration
SERVER_URL = "https://your-server-domain-or-ip:5000/ping"  # Use the secure HTTPS URL
API_KEY = "your-secure-api-key"  # The API key must match the one configured on the server
HOSTNAME = socket.gethostname()  # Automatically get the hostname of the host
INTERVAL = 300  # 5 minutes in seconds

def send_ping():
    headers = {'Authorization': f'Bearer {API_KEY}'}  # Include the API key in the headers
    try:
        response = requests.post(SERVER_URL, json={'hostname': HOSTNAME}, headers=headers, verify=True)
        if response.status_code == 200:
            print(f"Ping sent successfully from {HOSTNAME}")
        else:
            print(f"Failed to send ping from {HOSTNAME}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending ping from {HOSTNAME}: {e}")

if __name__ == "__main__":
    while True:
        send_ping()
        time.sleep(INTERVAL)
