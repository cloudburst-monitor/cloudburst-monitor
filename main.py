from flask import Flask, jsonify, send_from_directory
import serial
import time

app = Flask(__name__)

# 🔌 Arduino connect
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    print("✅ Arduino Connected")
except:
    arduino = None
    print("❌ Arduino NOT connected")

# 🔥 STATE VARIABLES
last_rain_value = 0
last_update_time = 0


# 📊 SENSOR READ
def get_sensor_data():
    global last_rain_value, last_update_time

    if arduino:
        try:
            readings = []

            # 🔥 ONLY CHANGE: read only latest clean value
            while arduino.in_waiting:
                value = arduino.readline().decode().strip()
                if value.isdigit():
                    readings = [int(value)]   # keep only latest

            if readings:
                rain_raw = sum(readings) / len(readings)

                # invert sensor
                rainfall = 1023 - rain_raw

                current_time = time.time()

                # SAME spike logic
                if rainfall > last_rain_value + 20 and rainfall < 900:

                    confirm = arduino.readline().decode().strip()

                    if confirm.isdigit():
                        confirm_val = 1023 - int(confirm)

                        if confirm_val > last_rain_value + 20:
                            last_rain_value = rainfall
                            last_update_time = current_time

                elif current_time - last_update_time < 12 and rainfall > 100:
                    rainfall = last_rain_value

                else:
                    last_rain_value = max(rainfall, last_rain_value * 0.9)
                    rainfall = last_rain_value

                rain_percent = (rainfall / 1023) * 100

                return rainfall, rain_percent

        except:
            pass

    return last_rain_value, (last_rain_value / 1023) * 100


# 🤖 AI LOGIC (UNCHANGED)
def predict_risk(rain_percent):

    if rain_percent < 20:
        return "Normal", 10
    elif rain_percent < 50:
        return "Risk", 40
    elif rain_percent < 80:
        return "Risk", 70
    else:
        return "High Risk", 95


# 🌐 ROUTES (UNCHANGED)
@app.route("/")
def home():
    return send_from_directory(".", "dashboard.html")


@app.route("/data")
def data():
    rainfall, rain_percent = get_sensor_data()

    risk, score = predict_risk(rain_percent)

    return jsonify({
        "rainfall": int(rainfall),
        "score": int(score),
        "risk": risk
    })


if __name__ == "__main__":
    app.run(debug=False)