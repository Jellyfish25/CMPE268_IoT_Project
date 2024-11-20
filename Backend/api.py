from flask import Flask, jsonify, request
from flask_cors import CORS

#All the hardware stuff
import hardware

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

#Starts hardware updates
hw = hardware.Hardware()
hw.start()

@app.route("/api/set_goal", methods=['POST'])
def set_goal_temp():
    try:
        hw.set_goal(request.get_json()["goal_temp"])
        return "", 200
    except Exception as e:
        return jsonify({"message": "Failed to receive data", "Error": str(e)}), 500

@app.route("/api/get_temperature", methods=['GET'])
def get_temperature():
    if hw.cur_temp:
        return jsonify({"temperature": hw.cur_temp}), 200
    else:
        return jsonify({"message": "No data from arduino yet"}), 404
    
@app.route("/api/start", methods=['POST'])
def start():
    hw.start()
    return "", 200

@app.route("/api/stop", methods=['POST'])
def stop():
    hw.stop()
    return "", 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
