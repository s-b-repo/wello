Example of a Systemd Service

If you want the script to run as a background service on a Linux system, you can create a systemd service file.

    Create a Service File:

    Create a file at /etc/systemd/system/host_monitor.service with the following content:

[Unit]
Description=Host Monitoring Service
After=network.target

[Service]
ExecStart=/usr/local/bin/host_monitor.py
Restart=always
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target

Enable and Start the Service:

Run the following commands to enable and start the service:



sudo systemctl daemon-reload
sudo systemctl enable host_monitor.service
sudo systemctl start host_monitor.service

Check the Service Status:

You can check the status of the service with:



sudo systemctl status host_monitor.service
