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

        # -----------------------------
        # UPDATED AI RISK LOGIC
        # -----------------------------
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

        # -----------------------------
        # INDIAN TIME
        # -----------------------------
        india = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(india).strftime("%I:%M:%S %p")

        # -----------------------------
        # FINAL DATA
        # -----------------------------
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
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():

    html = """

<!DOCTYPE html>
<html>

<head>

    <title>AI Cloudburst EWS</title>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet"
    href="https://unpkg.com/leaflet/dist/leaflet.css"/>

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<style>

body{
    margin:0;
    font-family:'Segoe UI',sans-serif;
    background:linear-gradient(to bottom,#031525,#0a2744);
    color:white;
    text-align:center;
}

h1{
    padding:25px;
    font-size:42px;
    font-weight:bold;
}

#map{
    height:420px;
    width:92%;
    margin:auto;
    border-radius:20px;
    overflow:hidden;
    box-shadow:0 0 25px rgba(0,0,0,0.5);
}

.cards{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    margin-top:25px;
    margin-bottom:30px;
}

.card{
    background: linear-gradient(145deg,#0b2d4d,#123d63);
    margin:15px;
    padding:30px;
    border-radius:20px;
    width:240px;
    box-shadow:0 8px 25px rgba(0,0,0,0.4);
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);
}

.card h2{
    margin:0;
    font-size:24px;
}

.value{
    font-size:42px;
    font-weight:bold;
    margin-top:20px;
}

.footer{
    margin-top:20px;
    padding-bottom:25px;
    opacity:0.8;
}

</style>

</head>

<body>

<h1>☁️ AI Cloudburst Early Warning System</h1>

<div id="map"></div>

<div class="cards">

    <div class="card">
        <h2>🌧 Rainfall</h2>
        <div class="value" id="rainfall">0</div>
    </div>

    <div class="card">
        <h2>🧠 AI Risk</h2>
        <div class="value" id="risk">0%</div>
    </div>

    <div class="card">
        <h2>⚠ Status</h2>
        <div class="value" id="status">Normal</div>
    </div>

    <div class="card">
        <h2>🕒 Time</h2>
        <div class="value" id="time">--:--</div>
    </div>

</div>

<div class="footer">
    Real-Time Hyperlocal Disaster Monitoring System
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

    document.getElementById("risk").innerHTML =
    data.risk + "%";

    document.getElementById("status").innerHTML =
    data.status;

    document.getElementById("time").innerHTML =
    data.time;

    // -----------------------------
    // STATUS COLOR
    // -----------------------------

    let statusElement =
    document.getElementById("status");

    if(data.status == "Normal Risk"){

        statusElement.style.color = "#00ff88";
    }

    else if(data.status == "Average Risk"){

        statusElement.style.color = "#ffd000";
    }

    else if(data.status == "High Risk"){

        statusElement.style.color = "#ff8800";
    }

    else{

        statusElement.style.color = "#ff3b3b";
    }

    // -----------------------------
    // MAP UPDATE
    // -----------------------------

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

    app.run(
        host="0.0.0.0",
        port=port
    )
