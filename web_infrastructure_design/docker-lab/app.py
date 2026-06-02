from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)
server_name = os.environ.get('SERVER_NAME', 'unknown')

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Holberton Web Infrastructure Lab!",
        "server": server_name,
        "hostname": socket.gethostname()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
