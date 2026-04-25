# =========================
# main.py
# =========================

from flask import Flask, jsonify, send_from_directory
import serial
import threading
import time
import os
import numpy as np
import joblib

app = Flask(__name__)

# =========================
# LOAD ML MODEL
# =========================

model = joblib.load("model.pkl")

# =========================
# SERIAL CONNECTION
# =========================

try:
    arduino = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)
    print("✅ ESP32 Connected")

except Exception as e:

    arduino = None
    print("❌ ESP32 NOT connected:", e)

# =========================
# GLOBAL VARIABLES
# =========================

last_rain_value = 0
last_score = 0
last_risk = "Normal"

# =========================
# RISK MAP
# =========================

risk_map = {

    0: ("Normal", 20),

    1: ("Risk", 65),

    2: ("High Risk", 95)
}

# =========================
# SENSOR LOOP
# =========================

def sensor_loop():

    global last_rain_value
    global last_score
    global last_risk

    while True:

        if arduino:

            try:

                if arduino.in_waiting > 0:

                    value = arduino.readline().decode(
                        errors='ignore'
                    ).strip()

                    if value.isdigit():

                        rain_raw = int(value)

                        rainfall = max(
                            0,
                            rain_raw * 0.03
                        )

                        if rainfall > 1:

                            # SMOOTHING
                            last_rain_value = round(

                                (last_rain_value * 0.7) +

                                (rainfall * 0.3),

                                2
                            )

                            # CONVERT TO %
                            rain_percent = min(

                                100,

                                (last_rain_value / 120) * 100
                            )

                            # ML PREDICTION
                            prediction = model.predict(

                                np.array([[rain_percent]])

                            )[0]

                            last_risk, last_score = risk_map[prediction]

            except Exception as e:

                print(e)

        time.sleep(0.1)

# =========================
# START THREAD
# =========================

threading.Thread(

    target=sensor_loop,
    daemon=True

).start()

# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():

    return send_from_directory(
        ".",
        "dashboard.html"
    )

# =========================
# DATA API
# =========================

@app.route("/data")
def data():

    return jsonify({

        "rainfall": round(last_rain_value, 2),

        "score": last_score,

        "risk": last_risk,

        "timestamp": time.strftime("%H:%M:%S")

    })

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",
        port=10000,
        debug=True
    )
