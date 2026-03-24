from flask import Flask, jsonify, send_from_directory, request
import serial
import time

app = Flask(__name__)

# 🔌 ESP32 connect
try:
    arduino = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)
    print("✅ ESP32 Connected")
except Exception as e:
    arduino = None
    print("❌ ESP32 NOT connected:", e)

# 🔥 STATE VARIABLES
last_rain_value = 0
last_update_time = 0


# 📊 SENSOR READ (UNCHANGED)
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


# 🌐 HOME ROUTE (UNCHANGED)
@app.route("/")
def home():
    return send_from_directory(".", "dashboard.html")


# 🔥 FIXED ROUTE (ONLY CHANGE = methods)
@app.route("/data", methods=["GET", "POST"])
def data():
    global last_rain_value

    # 🔹 POST (ESP32 / WiFi)
    if request.method == "POST":
        try:
            data = request.get_json()

            # अगर JSON नहीं आया तो fallback
            if not data:
                return jsonify({"status": "no data"}), 400

            last_rain_value = int(data.get("rainfall", 0))
            print("📥 Received:", last_rain_value)

            return jsonify({"status": "received"}), 200

        except Exception as e:
            print("POST Error:", e)
            return jsonify({"status": "error"}), 500

    # 🔹 GET (Dashboard / Serial fallback)
    rainfall, rain_percent = get_sensor_data()

    risk, score = predict_risk(rain_percent)

    return jsonify({
        "rainfall": int(rainfall),
        "score": int(score),
        "risk": risk
    })


# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=False)
