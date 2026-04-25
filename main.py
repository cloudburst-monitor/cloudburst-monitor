from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# 🌧 Global variables
latest_rainfall = 0
risk = 0
status = "Normal"

# 🇮🇳 Indian Time
india = pytz.timezone('Asia/Kolkata')

# =========================
# 🏠 DASHBOARD ROUTE
# =========================
@app.route('/')
def dashboard():

    global latest_rainfall, risk, status

    current_time = datetime.now(india).strftime("%H:%M:%S")

    html = f"""

    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Cloudburst Monitoring Dashboard</title>

        <meta http-equiv="refresh" content="5">

        <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet/dist/leaflet.css"
        />

        <script
        src="https://unpkg.com/leaflet/dist/leaflet.js">
        </script>

        <style>

            body {{
                margin: 0;
                padding: 0;
                background: #071c34;
                color: white;
                font-family: Arial;
                text-align: center;
            }}

            h1 {{
                padding: 20px;
            }}

            #map {{
                height: 450px;
                width: 95%;
                margin: auto;
                border-radius: 15px;
            }}

            .container {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 20px;
            }}

            .card {{
                background: #0e2a4d;
                width: 250px;
                margin: 15px;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
            }}

            .value {{
                font-size: 40px;
                font-weight: bold;
                margin-top: 20px;
            }}

        </style>
    </head>

    <body>

        <h1>☁ AI Cloudburst Monitoring Dashboard</h1>

        <div id="map"></div>

        <h2 style="margin-top:20px;">
            Sector 118, Mohali, Punjab, India
        </h2>

        <div class="container">

            <div class="card">
                <h2>Rainfall</h2>
                <div class="value">{latest_rainfall}</div>
            </div>

            <div class="card">
                <h2>AI Risk %</h2>
                <div class="value">{risk}%</div>
            </div>

            <div class="card">
                <h2>Status</h2>
                <div class="value">{status}</div>
            </div>

            <div class="card">
                <h2>Time</h2>
                <div class="value">{current_time}</div>
            </div>

        </div>

        <script>

            var map = L.map('map').setView([30.7046, 76.7179], 12);

            L.tileLayer(
                'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                {{
                    maxZoom: 19
                }}
            ).addTo(map);

            L.marker([30.7046, 76.7179])
            .addTo(map)
            .bindPopup("Cloudburst Monitoring Area")
            .openPopup();

        </script>

    </body>
    </html>

    """

    return render_template_string(html)

# =========================
# 📡 RECEIVE SENSOR DATA
# =========================
@app.route('/data', methods=['POST'])
def receive_data():

    global latest_rainfall, risk, status

    data = request.get_json()

    if data:

        latest_rainfall = data.get("rainfall", 0)

        # 🤖 AI Logic
        if latest_rainfall < 100:
            risk = 10
            status = "Normal"

        elif latest_rainfall < 500:
            risk = 55
            status = "Warning"

        else:
            risk = 95
            status = "DANGER"

        print("Received:", data)

        return jsonify({
            "message": "Data received successfully",
            "rainfall": latest_rainfall,
            "risk": risk,
            "status": status
        })

    return jsonify({
        "error": "No data received"
    }), 400

# =========================
# 🚀 RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)
