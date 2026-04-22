from flask import Flask, jsonify, send_from_directory, request
import serial
import time
import joblib
import os

app = Flask(__name__)

# ESP32 connect
try:
    arduino = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)
    print("ESP32 Connected")

except Exception as e:
    arduino = None
    print("ESP32 NOT connected:", e)


# LOAD ML MODEL
model = joblib.load("model.pkl")

# STATE VARIABLES
last_rain_value = 0
last_update_time = 0


# SENSOR READ
def get_sensor_data():

    global last_rain_value, last_update_time

    if arduino:

        try:
            readings = []

            while arduino.in_waiting:

                value = arduino.readline().decode(errors='ignore').strip()

                if value.isdigit():
                    readings = [int(value)]

            if readings:

                rain_raw = readings[-1]

                rainfall = 4095 - rain_raw

                current_time = time.time()

                if rainfall > last_rain_value + 20 and rainfall < 3800:

                    confirm = arduino.readline().decode(errors='ignore').strip()

                    if confirm.isdigit():

                        confirm_val = 4095 - int(confirm)

                        if confirm_val > last_rain_value + 20:

                            last_rain_value = rainfall
                            last_update_time = current_time

                elif current_time - last_update_time < 12 and rainfall > 100:

                    rainfall = last_rain_value

                else:

                    last_rain_value = max(rainfall, last_rain_value * 0.9)

                    rainfall = last_rain_value

                rain_percent = (rainfall / 4095) * 100

                return rainfall, rain_percent

        except Exception as e:

            print("Sensor Error:", e)

    return last_rain_value, (last_rain_value / 4095) * 100


# AI PREDICTION
def predict_risk(rain_percent):

    # 0 - 30
    if rain_percent <= 30:
        return "Normal", rain_percent

    # 31 - 50
    elif rain_percent <= 50:
        return "Average", rain_percent

    # 51 - 80
    elif rain_percent <= 80:
        return "Risk", rain_percent

    # 81 - 100
    else:
        return "High Risk", min(100, rain_percent)


# HOME ROUTE
@app.route("/")
def home():

    return send_from_directory(".", "dashboard.html")


# DATA API
@app.route("/data", methods=["GET", "POST"])
def data():

    global last_rain_value

    # ESP32 POST
    if request.method == "POST":

        try:
            data = request.get_json(force=True)

            if data and "rainfall" in data:

                last_rain_value = int(data["rainfall"])

                print("Received:", last_rain_value)

        except Exception as e:

            print("POST Error:", e)

        return jsonify({
            "status": "received"
        })

    # Dashboard GET
    rainfall = last_rain_value

    rain_percent = (rainfall / 4095) * 100

    risk, score = predict_risk(rain_percent)

    return jsonify({
        "rainfall": int(rainfall),
        "score": round(float(score), 2),
        "risk": risk
    })


# RUN SERVER
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
