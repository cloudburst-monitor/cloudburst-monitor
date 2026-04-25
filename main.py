from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):

    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():

    return send_from_directory(".", "dashboard.html")

# -----------------------------
# RECEIVE SENSOR DATA
# -----------------------------
@app.route("/data", methods=["POST"])
def receive_data():

    try:

        data = request.get_json()

        raw_value = data.get("rainfall", 0)

        # SENSOR CONVERSION
        rainfall = int(raw_value / 40)

        if rainfall < 0:
            rainfall = 0

        # AI RISK LOGIC
        if rainfall <= 20:

            risk = 15
            status = "Normal Risk"

        elif rainfall <= 50:

            risk = 45
            status = "Average Risk"

        elif rainfall <= 80:

            risk = 75
            status = "High Risk"

        else:

            risk = 95
            status = "Extreme Danger"

        india = pytz.timezone("Asia/Kolkata")

        current_time = datetime.now(india).strftime(
            "%I:%M:%S %p"
        )

        final_data = {

            "rainfall": rainfall,
            "risk": risk,
            "status": status,
            "time": current_time,
            "lat": 30.7046,
            "lon": 76.7179
        }

        with open(DATA_FILE, "w") as f:
            json.dump(final_data, f)

        return jsonify({
            "message": "success"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# GET DATA
# -----------------------------
@app.route("/getdata")
def get_data():

    try:

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        return jsonify(data)

    except:

        return jsonify({

            "rainfall": 0,
            "risk": 0,
            "status": "No Data",
            "time": "--:--",
            "lat": 30.7046,
            "lon": 76.7179
        })

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
