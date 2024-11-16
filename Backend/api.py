from flask import Flask, jsonify, request
from flask_cors import CORS
import serial
import time
from threading import Thread

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PRIVATE_IPV4 = "127.0.0.1" #currently set to localhost
serConn = serial.Serial("/dev/cu.usbmodem14301", 9600, timeout=1)
temperature_data = None
# @app.route("/api/set_temperature", methods=['POST'])
# def send_temperature_data():
#     try:
#         data = request.get_json()
#         return jsonify({"message": "Data has been received", "received_data": data}), 200
#     except Exception as e:
#         return jsonify({"message": "Failed to receive data", "Error": str(e)}), 500

def read_from_serial():
    global temperature_data
    while True:
        if serConn.in_waiting > 0:
            data = serConn.readline().decode('utf-8').strip()
            print(f"retrieved data: {data}")
            if "Temperature:" in data:
                temperature_data = data.split(":")[1].strip()
                print(f"Received temperature:{temperature_data}")
        time.sleep(1)

serial_thread = Thread(target=read_from_serial)
serial_thread.daemon = True
serial_thread.start()

@app.route("/api/get_temperature", methods=['Get'])
def get_temperature():
    if temperature_data:
        return jsonify({"temperature": temperature_data}), 200
    else:
        return jsonify({"message": "No data from arduino yet"}), 404
    
if __name__ == "__main__":
    app.run(host=PRIVATE_IPV4, port=5000)
