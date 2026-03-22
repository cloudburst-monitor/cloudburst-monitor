from flask import Flask, jsonify, send_from_directory
import random

app = Flask(__name__)

# 🔹 GLOBAL VALUE (smooth changes ke liye)
last_value = 20

# 🔹 SENSOR FUNCTION (stable)
def get_sensor_data():
    global last_value
    
    change = random.randint(-2, 2)  # small variation
    last_value = max(0, min(100, last_value + change))
    
    return last_value, last_value

# 🔹 RISK PREDICTION (stable logic)
def predict_risk(rain_percent):
    if rain_percent > 80:
        return "HIGH", 95
    elif rain_percent > 60:
        return "MEDIUM", 70
    else:
        return "LOW", 30

# 🔹 ROUTES
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

# 🔹 MAIN RUN
if __name__ == "__main__":
    print("🚀 Server starting...")
    app.run(host="0.0.0.0", port=10000)
