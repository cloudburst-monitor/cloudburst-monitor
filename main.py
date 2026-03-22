from flask import Flask, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

# 🔹 Dummy sensor data (since Arduino not connected on cloud)
def get_sensor_data():
    rainfall = random.randint(0, 100)
    rain_percent = rainfall
    return rainfall, rain_percent

# 🔹 Prediction logic
def predict_risk(rain_percent):
    if rain_percent > 80:
        return "HIGH", 95
    elif rain_percent > 50:
        return "MEDIUM", 70
    else:
        return "LOW", 40

# 🔹 Route for dashboard
@app.route("/")
def home():
    return send_from_directory(".", "dashboard.html")

# 🔹 API route
@app.route("/data")
def data():
    rainfall, rain_percent = get_sensor_data()
    risk, score = predict_risk(rain_percent)

    return jsonify({
        "rainfall": int(rainfall),
        "score": int(score),
        "risk": risk
    })

# 🔥 IMPORTANT: Render compatible run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
