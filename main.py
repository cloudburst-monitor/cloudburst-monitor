from flask import Flask, jsonify, send_from_directory, request
import time

app = Flask(__name__)

# 🔥 STATE VARIABLES
last_rain_value = 0
last_update_time = 0


# 📊 SENSOR LOGIC (same structure, serial हटाया)
def get_sensor_data():
    global last_rain_value, last_update_time

    current_time = time.time()

    # fallback smoothing logic (same idea)
    rainfall = last_rain_value

    if current_time - last_update_time < 12 and rainfall > 100:
        rainfall = last_rain_value
    else:
        last_rain_value = (last_rain_value * 0.7) + (rainfall * 0.3)
        rainfall = last_rain_value

    rain_percent = (rainfall / 4095) * 100

    return rainfall, rain_percent


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


# 🌐 HOME
@app.route("/")
def home():
    return send_from_directory(".", "dashboard.html")


# 🔥 MAIN ROUTE (GET + POST)
@app.route("/data", methods=["GET", "POST"])
def data():
    global last_rain_value, last_update_time

    # 🟢 ESP32 → POST
    if request.method == "POST":
        try:
            data = request.get_json()

            if not data:
                return jsonify({"status": "no data"}), 400

            last_rain_value = int(data.get("rainfall", 0))
            last_update_time = time.time()

            print("📥 Received:", last_rain_value)

            return jsonify({"status": "received"}), 200

        except Exception as e:
            print("POST Error:", e)
            return jsonify({"status": "error"}), 500

    # 🔵 Dashboard → GET
    rainfall, rain_percent = get_sensor_data()
    risk, score = predict_risk(rain_percent)

    return jsonify({
        "rainfall": int(rainfall),
        "score": int(score),
        "risk": risk
    })


# 🚀 RUN (Render compatible)
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
