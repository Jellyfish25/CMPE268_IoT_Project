from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PRIVATE_IPV4 = "127.0.0.1" #currently set to localhost

# @app.route("/api/set_temperature", methods=['POST'])
# def send_temperature_data():
#     try:
#         data = request.get_json()
#         return jsonify({"message": "Data has been received", "received_data": data}), 200
#     except Exception as e:
#         return jsonify({"message": "Failed to receive data", "Error": str(e)}), 500

@app.route("/api/get_temperature", methods=['GET'])
def get_temperature_data():
    data = {"temperature": 63}
    return data, 200

if __name__ == "__main__":
    app.run(host=PRIVATE_IPV4, port=5000)
