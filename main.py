from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# -----------------------------
# CREATE FILE IF NOT EXISTS
# -----------------------------
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return dashboard()

# -----------------------------
# RECEIVE SENSOR DATA FROM ESP32
# -----------------------------
@app.route("/data", methods=["POST"])
def receive_data():
    try:
        data = request.get_json()

        rainfall = data.get("rainfall", 0)

        # AI Risk Calculation
        if rainfall < 30:
            risk = 10
            status = "Normal"

        elif rainfall < 70:
            risk = 55
            status = "Warning"

        else:
            risk = 95
            status = "DANGER"

        # Indian Time
        india = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(india).strftime("%I:%M:%S %p")

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
            "message": "Data received successfully",
            "risk": risk,
            "status": status
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# GET DATA FOR DASHBOARD
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
            "time": "--:--:--",
            "lat": 30.7046,
            "lon": 76.7179
        })


# -----------------------------
# DASHBOARD UI
# -----------------------------
@app.route("/dashboard")
def dashboard():

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Cloudburst Monitoring Dashboard</title>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link rel="stylesheet"
        href="https://unpkg.com/leaflet/dist/leaflet.css"/>

        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

        <style>

            body{
                margin:0;
                font-family:Arial;
                background:#071b2f;
                color:white;
                text-align:center;
            }

            h1{
                padding:20px;
            }

            #map{
                height:400px;
                width:90%;
                margin:auto;
                border-radius:15px;
            }

            .cards{
                display:flex;
                flex-wrap:wrap;
                justify-content:center;
                margin-top:20px;
            }

            .card{
                background:#0f2f4f;
                margin:10px;
                padding:25px;
                border-radius:15px;
                width:220px;
                box-shadow:0px 0px 10px rgba(0,0,0,0.5);
            }

            .value{
                font-size:40px;
                font-weight:bold;
                margin-top:15px;
            }

        </style>
    </head>

    <body>

        <h1>☁️ AI Cloudburst Monitoring Dashboard</h1>

        <div id="map"></div>

        <div class="cards">

            <div class="card">
                <h2>Rainfall</h2>
                <div class="value" id="rainfall">0</div>
            </div>

            <div class="card">
                <h2>AI Risk %</h2>
                <div class="value" id="risk">0%</div>
            </div>

            <div class="card">
                <h2>Status</h2>
                <div class="value" id="status">Normal</div>
            </div>

            <div class="card">
                <h2>Time</h2>
                <div class="value" id="time">--:--</div>
            </div>

        </div>

        <script>

            var map = L.map('map').setView([30.7046, 76.7179], 12);

            L.tileLayer(
                'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                {
                    attribution:'© OpenStreetMap'
                }
            ).addTo(map);

            var marker = L.marker([30.7046, 76.7179]).addTo(map);

            async function fetchData(){

                let response = await fetch('/getdata');
                let data = await response.json();

                document.getElementById("rainfall").innerHTML = data.rainfall;
                document.getElementById("risk").innerHTML = data.risk + "%";
                document.getElementById("status").innerHTML = data.status;
                document.getElementById("time").innerHTML = data.time;

                marker.setLatLng([data.lat, data.lon]);

                map.setView([data.lat, data.lon], 12);
            }

            fetchData();

            setInterval(fetchData, 3000);

        </script>

    </body>
    </html>
    """

    return render_template_string(html)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
