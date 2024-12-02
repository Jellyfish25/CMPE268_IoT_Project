import socket
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ESP32 Details
esp32_ip = "10.0.0.178"
port = 80

# Helper function to send socket requests
def send_socket_request(message):
    try:
        with socket.create_connection((esp32_ip, port), timeout=5) as sock:
            sock.sendall(message.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        return str(e)

@app.route("/api/light", methods=['POST'])
def toggle_light():
    try:
        lightStatus = request.get_json()["light_status"]
        lightStatusStr = str(lightStatus)
        message = f"POST /api/light HTTP/1.1\r\nHost: ESP32\r\nContent-Length: {len(lightStatusStr)}\r\n\r\n{lightStatusStr}"
        response = send_socket_request(message)
        return jsonify({"message": "Light updated", "response": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to update light", "error": str(e)}), 400

@app.route("/api/goal", methods=['POST'])
def set_goal_temp():
    try:
        goal_temp = request.get_json()["goal_temp"]
        goal_temp_str = str(goal_temp)
        message = f"POST /api/goal HTTP/1.1\r\nHost: ESP32\r\nContent-Length: {len(goal_temp_str)}\r\n\r\n{goal_temp_str}"

        # Send the message to the ESP32 via socket
        response = send_socket_request(message)
        return jsonify({"message": "Temperature updated", "response": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to update temperature", "error": str(e)}), 400


@app.route("/api/start_time", methods=['POST'])
def set_start_time():
    try:
        start_time = request.get_json()["start_time"]
        message = f"POST /api/start_time HTTP/1.1\r\nHost: ESP32\r\nContent-Length: {len(start_time)}\r\n\r\n{start_time}"
        response = send_socket_request(message)
        return jsonify({"start_time updated": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400


@app.route("/api/end_time", methods=['POST'])
def set_end_time():
    try:
        end_time = request.get_json()["end_time"]
        message = f"POST /api/end_time HTTP/1.1\r\nHost: ESP32\r\nContent-Length: {len(end_time)}\r\n\r\n{end_time}"
        response = send_socket_request(message)
        return jsonify({"end_time updated": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400


@app.route("/api/times", methods=['POST'])
def set_times():
    try:
        start_time = request.get_json()["start_time"]
        end_time = request.get_json()["end_time"]
        start_message = f"POST /api/start_time HTTP/1.1\r\nHost: ESP32\r\nContent-Length: {len(start_time)}\r\n\r\n{start_time}"
        end_message = f"POST /api/end_time HTTP/1.1\r\nHost: ESP32\r\nContent-Length: {len(end_time)}\r\n\r\n{end_time}"

        # Send both start and end time messages to ESP32
        send_socket_request(start_message)
        send_socket_request(end_message)
        return "", 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400


@app.route("/api/start", methods=['POST'])
def start():
    try:
        message = "POST /api/start HTTP/1.1\r\nHost: ESP32\r\n\r\n"
        response = send_socket_request(message)
        return jsonify({"message": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to start", "Error": str(e)}), 400


@app.route("/api/stop", methods=['POST'])
def stop():
    try:
        message = "POST /api/stop HTTP/1.1\r\nHost: ESP32\r\n\r\n"
        response = send_socket_request(message)
        return jsonify({"message": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to stop", "Error": str(e)}), 400


@app.route("/api/get_temperature", methods=['GET'])
def get_temperature():
    try:
        response = requests.get(f"http://{esp32_ip}/api/get_temperature")
        
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            temperature = data.get("temperature", None)
            
            if temperature is None:
                return jsonify({"message": "Temperature data is missing in the response"}), 500

            return jsonify({"temperature": temperature}), 200
        else:
            return jsonify({"message": "Failed to retrieve temperature from ESP32"}), 500
    
    except Exception as e:
        return jsonify({"message": "Failed to retrieve temperature", "Error": str(e)}), 400


@app.route("/api/times", methods=['GET'])
def get_times():
    try:
        message = "GET /api/times HTTP/1.1\r\nHost: ESP32\r\n\r\n"
        response = send_socket_request(message)
        return jsonify({"times": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve times", "Error": str(e)}), 400


@app.route("/api/status", methods=['GET'])
def get_status():
    try:
        message = "GET /api/status HTTP/1.1\r\nHost: ESP32\r\n\r\n"
        response = send_socket_request(message)
        return jsonify({"status": response}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve status", "Error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
