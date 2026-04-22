from flask import Flask, jsonify, send_from_directory
import serial
import threading
import time
import os

app = Flask(__name__)

# ESP32 CONNECT
arduino = None

try:

    arduino = serial.Serial(
        'COM6',
        115200,
        timeout=1
    )

    time.sleep(2)

    print("ESP32 Connected")

except Exception as e:

    print("Running without ESP32")


# GLOBAL VALUES
last_rain_value = 0
last_risk = "Normal"
last_score = 0


# BACKGROUND SENSOR READER
def sensor_loop():

    global last_rain_value
    global last_risk
    global last_score

    while True:

        if arduino:

            try:

                if arduino.in_waiting > 0:

                    value = arduino.readline().decode(
                        errors='ignore'
                    ).strip()

                    if value.isdigit():

                        rain_raw = int(value)

                        # SENSOR CALIBRATION
                        rainfall = max(
                            0,
                            rain_raw * 0.03
                        )

                        # Ignore tiny/noise readings
                        if rainfall > 5:

                            # SMOOTH GRAPH VALUES
                            last_rain_value = round(
                                (last_rain_value * 0.2) +
                                (rainfall * 0.8),
                                2
                            )

                            # PERCENTAGE SCALING
                            rain_percent = min(
                                100,
                                (last_rain_value / 120) * 100
                            )

                            last_score = round(
                                rain_percent,
                                2
                            )

                            # RISK LOGIC
                            if rain_percent <= 30:

                                last_risk = "Normal"

                            elif rain_percent <= 70:

                                last_risk = "Average"

                            elif rain_percent < 85:

                                last_risk = "Risk"

                            else:

                                last_risk = "High Risk"

            except Exception:

                pass

        # FAST RESPONSE
        time.sleep(0.05)


# START SENSOR THREAD
threading.Thread(
    target=sensor_loop,
    daemon=True
).start()


# HOME ROUTE
@app.route("/")
def home():

    return send_from_directory(
        ".",
        "dashboard.html"
    )


# API ROUTE
@app.route("/data")
def data():

    return jsonify({

        "rainfall": last_rain_value,

        "score": last_score,

        "risk": last_risk

    })


# RUN SERVER
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
