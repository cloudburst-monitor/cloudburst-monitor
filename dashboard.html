<!-- =========================
dashboard.html
========================= -->

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Cloudburst Monitoring System</title>

<link rel="stylesheet"
href="https://unpkg.com/leaflet/dist/leaflet.css"/>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{

    margin:0;
    font-family:'Segoe UI',sans-serif;
    background:#071421;
    color:white;
}

.header{

    text-align:center;
    padding:18px;
    font-size:28px;
    font-weight:bold;
    background:#10263d;
}

.alert-bar{

    display:none;
    background:red;
    text-align:center;
    padding:12px;
    font-weight:bold;
}

#map{

    height:350px;
    width:95%;
    margin:15px auto;
    border-radius:12px;
}

.location{

    text-align:center;
    color:#bbbbbb;
}

.cards{

    display:flex;
    justify-content:space-between;
    gap:15px;
    margin:20px;
    flex-wrap:wrap;
}

.card{

    flex:1;
    min-width:180px;

    background:#112b45;

    padding:18px;

    border-radius:12px;

    text-align:center;
}

.card p{

    font-size:26px;
    font-weight:bold;
}

.normal{

    color:#00ff88;
}

.risk{

    color:orange;
}

.high{

    color:red;
}

.alerts{

    margin:20px;
}

.alert-item{

    background:#132f4c;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;

    display:flex;
    justify-content:space-between;
}

canvas{

    background:#112b45;
    border-radius:12px;
    padding:10px;
}

</style>
</head>

<body>

<div class="header">

☁ AI Cloudburst Monitoring Dashboard

</div>

<div class="alert-bar" id="alertBar">

⚠ HIGH RISK ALERT ⚠

</div>

<div id="map"></div>

<div class="location" id="locationText">

Detecting location...

</div>

<div class="cards">

    <div class="card">

        Rainfall

        <p id="rain">0</p>

    </div>

    <div class="card">

        AI Risk %

        <p id="risk">0%</p>

    </div>

    <div class="card">

        Status

        <p id="status">Normal</p>

    </div>

    <div class="card">

        Time

        <p id="time">--</p>

    </div>

</div>

<div style="width:90%; margin:auto;">

    <canvas id="rainChart"></canvas>

</div>

<div class="alerts">

    <h2>⚠ Active Alerts</h2>

    <div id="alertList"></div>

</div>

<script>



// =========================
// MAP
// =========================

let map = L.map('map').setView(
    [30.7333,76.7794],
    13
);

L.tileLayer(

'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

).addTo(map);

let userMarker = L.marker(
    [30.7333,76.7794]
).addTo(map);

navigator.geolocation.getCurrentPosition(

async(pos)=>{

    let lat = pos.coords.latitude;
    let lon = pos.coords.longitude;

    map.setView([lat,lon],13);

    userMarker.setLatLng([lat,lon]);

    let res = await fetch(

`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`

    );

    let data = await res.json();

    document.getElementById(
        "locationText"
    ).innerText = data.display_name;
});



// =========================
// CHART
// =========================

let rainData = [];
let labels = [];

const ctx = document
.getElementById("rainChart")
.getContext("2d");

const rainChart = new Chart(ctx, {

    type:"line",

    data:{

        labels:labels,

        datasets:[{

            label:"Rainfall Trend",

            data:rainData,

            borderColor:"cyan",

            backgroundColor:
            "rgba(0,255,255,0.1)",

            fill:true,

            tension:0.4
        }]
    },

    options:{

        responsive:true,

        plugins:{

            legend:{

                labels:{
                    color:"white"
                }
            }
        },

        scales:{

            x:{
                ticks:{
                    color:"white"
                }
            },

            y:{
                ticks:{
                    color:"white"
                },

                beginAtZero:true
            }
        }
    }
});



// =========================
// FETCH API DATA
// =========================

async function fetchData(){

    try{

        const response = await fetch("/data");

        const data = await response.json();

        document.getElementById(
            "rain"
        ).innerText = data.rainfall;

        document.getElementById(
            "risk"
        ).innerText = data.score + "%";

        document.getElementById(
            "time"
        ).innerText = data.timestamp;

        let status =
        document.getElementById("status");

        status.innerText = data.risk;

        status.className = "";

        if(data.risk === "Normal"){

            status.classList.add("normal");

            document.getElementById(
                "alertBar"
            ).style.display = "none";
        }

        else if(data.risk === "Risk"){

            status.classList.add("risk");

            document.getElementById(
                "alertBar"
            ).style.display = "none";
        }

        else{

            status.classList.add("high");

            document.getElementById(
                "alertBar"
            ).style.display = "block";
        }

        // UPDATE GRAPH

        rainData.push(data.rainfall);

        labels.push(data.timestamp);

        if(rainData.length > 15){

            rainData.shift();
            labels.shift();
        }

        rainChart.data.labels = labels;

        rainChart.data.datasets[0].data =
        rainData;

        rainChart.update();

        // ALERTS

        let html = `

        <div class="alert-item">

            <span>📍 Local Sensor Node</span>

            <span>${data.risk}</span>

            <span>${data.timestamp}</span>

        </div>

        `;

        document.getElementById(
            "alertList"
        ).innerHTML = html;

    }

    catch(error){

        console.log(error);
    }
}

// AUTO UPDATE

setInterval(fetchData,1000);

fetchData();

</script>

</body>
</html>
