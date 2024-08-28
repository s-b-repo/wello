Deployment Instructions

    Copy the Updated Script to Each Host:
        Save the script to a suitable location on each host, for example, /usr/local/bin/host_monitor.py.

    Make the Script Executable:
        Ensure the script has execute permissions:

       

    chmod +x /usr/local/bin/host_monitor.py

Run the Script:

    You can run the script manually or set it up to run automatically using a cron job or a systemd service.

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

    API Key Verification:
        The API key is checked in the Authorization header of each request to ensure only authorized clients can access the /ping endpoint.
        If the API key is incorrect or missing, a 401 Unauthorized response is returned.

    Ping Request Handling:
        The /ping endpoint only accepts POST requests. The client must send the hostname of the host in the JSON payload.
        The server records the current time as the last ping time for the host.

    Method Restriction:
        The /ping endpoint rejects any non-POST requests (like GET, PUT, DELETE, etc.) by returning a 405 Method Not Allowed response.

    Host Status Endpoint:
        The /status endpoint is available to view the last ping time of each host. This can be useful for debugging or monitoring but should be secured in production.

4. Running the API

    Save the above code to a file named secure_ping_api.py.
    Run the script:

bash

python secure_ping_api.py

5. Testing the API

You can use curl, Postman, or any other HTTP client to test the API.

Example Ping Request:

bash

curl -X POST http://localhost:5000/ping \
-H "Authorization: Bearer your-secure-api-key" \
-H "Content-Type: application/json" \
-d '{"hostname": "test-host"}'

This should return:

json

{"message": "Ping received"}

Testing Invalid Method:

bash

curl -X GET http://localhost:5000/ping \
-H "Authorization: Bearer your-secure-api-key"

This should return:

json

{"error": "Method not allowed"}

6. Deploying the API

    Production Setup: When deploying to production, use a WSGI server like Gunicorn or uWSGI and consider securing the API with HTTPS. You may also want to integrate with a reverse proxy like Nginx.

    Environment Variables: Store your API key securely using environment variables or a secrets management service.

