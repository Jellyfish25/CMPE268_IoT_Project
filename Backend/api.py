from flask import Flask, jsonify, request
from flask_cors import CORS

#All the hardware stuff
import hardware

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

#Initializes hardware stuff
hw = hardware.Hardware()

@app.route("/api/goal", methods=['POST'])
def set_goal_temp():
    try:
        hw.set_goal(request.get_json()["goal_temp"])
        return "", 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400
    
@app.route("/api/start_time", methods=['POST'])
def set_start_time():
    try:
        hw.set_start(request.get_json()["start_time"])
        return "", 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400
    
@app.route("/api/end_time", methods=['POST'])
def set_end_time():
    try:
        hw.set_end(request.get_json()["end_time"])
        return "", 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400
    
@app.route("/api/times", methods=['POST'])
def set_times():
    try:
        hw.set_start(request.get_json()["start_time"])
        hw.set_end(request.get_json()["end_time"])
        return "", 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 400
    
@app.route("/api/start", methods=['POST'])
def start():
    hw.start()
    return "", 200

@app.route("/api/stop", methods=['POST'])
def stop():
    hw.stop()
    return "", 200

#Redundant get_ to keep consistent with frontend
@app.route("/api/get_temperature", methods=['GET'])
def get_temperature():
    if hw.cur_temp:
        return jsonify({"temperature": hw.cur_temp, "goal": hw.goal_temp}), 200
    else:
        return jsonify({"message": "No data from arduino yet"}), 404
    
@app.route("/api/times", methods=['GET'])
def get_times():
    return jsonify({"start_time": hw.start_time, "end_time": hw.end_time, "updated_time": hw.updated_time}), 200

@app.route("/api/status", methods=['GET'])
def get_status():
    if hw.enabled:
        return jsonify({"device_status": "On", "fan_speed": hw.get_cur_speed()}), 200
    else:
        return jsonify({"device_status": "Off"}), 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
