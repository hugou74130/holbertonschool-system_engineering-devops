#!/bin/bash
# Provision Web Server (Nginx + Flask App)
set -e

apt-get update
apt-get install -y nginx python3 python3-pip python3-venv

# Create a simple Flask app
mkdir -p /var/www/app
cat > /var/www/app/app.py << 'EOF'
from flask import Flask, jsonify
import socket
app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Holberton Web Infrastructure Lab!",
        "server": socket.gethostname()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Create systemd service for Flask app
cat > /etc/systemd/system/flask-app.service << 'EOF'
[Unit]
Description=Flask Application Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/app
Environment="PATH=/var/www/app/venv/bin"
ExecStart=/var/www/app/venv/bin/python /var/www/app/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Setup Python venv and install Flask
python3 -m venv /var/www/app/venv
/var/www/app/venv/bin/pip install flask

# Configure Nginx as reverse proxy
cat > /etc/nginx/sites-available/default << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Start services
systemctl daemon-reload
systemctl start flask-app
systemctl enable flask-app
systemctl restart nginx
systemctl enable nginx

echo "Web server configured. Flask app running via Nginx reverse proxy."
