from flask import Flask, request, render_template_string
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
import json

app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Atmos — Live Weather</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{color-scheme:dark;--ink:#f5f7ff;--muted:#aab8d4;--line:#ffffff20;--cyan:#9cecff}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;color:var(--ink);font-family:'DM Sans',sans-serif;background:radial-gradient(ellipse at 15% 0%,#253c75 0%,transparent 38%),radial-gradient(ellipse at 100% 50%,#3d236d 0%,transparent 34%),#070d1c;overflow-x:hidden}
body:before,body:after{content:"";position:fixed;width:480px;height:480px;border-radius:50%;filter:blur(100px);opacity:.22;pointer-events:none;z-index:-1;animation:aurora 28s cubic-bezier(.45,0,.55,1) infinite alternate}
body:before{background:#3b8dff;top:-200px;left:-140px}body:after{background:#aa65ff;right:-220px;top:30%;animation-delay:-8s}
@keyframes aurora{from{transform:translate(0,0) scale(1)}to{transform:translate(85px,60px) scale(1.18)}}
.sky{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:-1}.sky i{position:absolute;display:block;width:220px;height:75px;background:#c4d8ff0b;border-radius:100px;filter:blur(2px);animation:cloud-drift 58s linear infinite}.sky i:before,.sky i:after{content:"";position:absolute;background:inherit;border-radius:50%}.sky i:before{width:90px;height:90px;left:35px;top:-42px}.sky i:after{width:125px;height:115px;left:85px;top:-55px}.sky i:nth-child(1){top:18%;left:-250px}.sky i:nth-child(2){top:55%;left:-300px;transform:scale(.7);animation-delay:-20s}.sky i:nth-child(3){top:78%;left:-260px;transform:scale(.5);animation-delay:-8s}
@keyframes cloud-drift{from{translate:0 0}to{translate:calc(100vw + 600px) 20px}}
main{width:min(1120px,calc(100% - 36px));margin:0 auto;padding:28px 0 24px;animation:enter 1.05s cubic-bezier(.22,1,.36,1) both}@keyframes enter{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:25px;gap:12px}.brand{font:800 23px Manrope,sans-serif;letter-spacing:-1px;display:flex;align-items:center;gap:10px}.brandmark{width:42px;height:42px;border-radius:15px;display:grid;place-items:center;background:linear-gradient(135deg,#92efff,#a79aff);color:#10172e;font-size:23px;box-shadow:0 8px 32px #71dfff3b}.live{font-size:11px;letter-spacing:1px;color:#aef4d4;border:1px solid #6de0b144;background:#43c99412;padding:9px 13px;border-radius:30px;display:flex;align-items:center;gap:8px}.dot{width:7px;height:7px;border-radius:50%;background:#68e4aa;box-shadow:0 0 12px #68e4aa;animation:pulse 1.8s infinite}@keyframes pulse{50%{opacity:.4;transform:scale(.78)}}
.search{display:flex;gap:10px;margin-bottom:22px}input{min-width:0;flex:1;background:#101b31d9;border:1px solid var(--line);border-radius:16px;padding:16px 18px;color:white;font:inherit;outline:none;box-shadow:0 10px 35px #00012}input:focus{border-color:#91ecff99;box-shadow:0 0 0 4px #91ecff10}button{border:0;border-radius:16px;padding:0 23px;background:linear-gradient(120deg,#9af0ff,#aaa0ff);color:#10162c;font:700 14px 'DM Sans',sans-serif;cursor:pointer;transition:transform .45s cubic-bezier(.22,1,.36,1),filter .45s ease,box-shadow .45s ease;box-shadow:0 8px 24px #8b9dff24}button:hover{transform:translateY(-2px);filter:brightness(1.08)}
.glass{background:linear-gradient(135deg,#ffffff14,#ffffff07);border:1px solid var(--line);border-radius:26px;box-shadow:0 24px 80px #0002;backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px)}.hero{padding:32px 36px;position:relative;overflow:hidden;margin-bottom:17px;isolation:isolate}.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 85% 30%,#7bcbff18,transparent 40%),linear-gradient(110deg,#7ebeff08,transparent 60%);z-index:-1}.hero:after{content:"";position:absolute;width:280px;height:280px;right:-60px;top:-110px;border-radius:50%;background:#86dfff12;filter:blur(5px);pointer-events:none;z-index:-1}.hero-top{display:flex;justify-content:space-between;align-items:center;gap:20px;position:relative;z-index:1}.eyebrow{font-size:11px;letter-spacing:2.2px;text-transform:uppercase;color:#9db1d3;font-weight:700}.location{font:700 clamp(23px,4vw,33px) Manrope,sans-serif;letter-spacing:-1px;margin-top:9px}.condition{color:#c6d5ee;margin-top:7px;font-size:16px}.temp-line{display:flex;align-items:center;gap:14px;margin-top:14px}.temp{font:800 clamp(76px,12vw,116px)/.98 Manrope,sans-serif;letter-spacing:-8px;background:linear-gradient(135deg,#fff 20%,#a7eaff 70%,#c2b5ff);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 10px 28px #9beaff12)}.weather-icon{font-size:clamp(76px,10vw,106px);filter:drop-shadow(0 12px 28px #7acfff40);animation:weather-float 6s cubic-bezier(.45,0,.55,1) infinite}@keyframes weather-float{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-12px) rotate(4deg)}}.feels{color:var(--muted);margin-top:14px}.updated{color:#8295b7;font-size:12px;margin-top:15px}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:20px}.metric{padding:20px 21px;position:relative;overflow:hidden;transition:transform .5s cubic-bezier(.22,1,.36,1),border-color .45s ease,box-shadow .45s ease,background .45s ease}.metric:after{content:"";position:absolute;width:90px;height:90px;border-radius:50%;right:-45px;bottom:-55px;background:#8adfff13;filter:blur(5px)}.metric:hover,.hour:hover,.day:hover{transform:translateY(-4px);border-color:#9beaff55}.metric-icon{font-size:20px;margin-bottom:14px}.metric-label{font-size:11px;letter-spacing:1.1px;color:var(--muted);font-weight:700}.metric-value{font:700 23px Manrope,sans-serif;margin-top:8px;letter-spacing:-.7px}
.section{padding:25px;margin-bottom:18px}.section-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:20px}h2{font:700 18px Manrope,sans-serif;margin:0;letter-spacing:-.4px}.section-sub{font-size:12px;color:var(--muted)}.hours{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}.hour{text-align:center;padding:17px 7px;border:1px solid #ffffff15;background:linear-gradient(160deg,#111f39d9,#0c1830a8);border-radius:18px;transition:transform .5s cubic-bezier(.22,1,.36,1),border-color .45s ease,box-shadow .45s ease,background .45s ease}.hour-time{font-size:12px;color:var(--muted)}.hour-icon{font-size:28px;margin:14px 0;filter:drop-shadow(0 4px 10px #8ddcff23)}.hour-temp{font:700 18px Manrope,sans-serif}.hour-rain{font-size:11px;color:var(--cyan);margin-top:9px}.days{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.day{padding:19px;border:1px solid #ffffff15;border-radius:19px;background:linear-gradient(160deg,#111f39d9,#0c1830a8);transition:transform .5s cubic-bezier(.22,1,.36,1),border-color .45s ease,box-shadow .45s ease,background .45s ease}.day-date{font-weight:700}.day-condition{color:var(--muted);font-size:12px;margin-top:6px}.day-bottom{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:17px}.day-icon{font-size:31px;filter:drop-shadow(0 4px 10px #8ddcff23)}.day-range{font:700 15px Manrope,sans-serif}.day-rain{font-size:11px;color:var(--cyan);margin-top:11px}.error{color:#ffb5c0;background:#ff617412;border:1px solid #ff61742b;padding:13px 15px;border-radius:13px;margin-bottom:15px;overflow-wrap:anywhere}footer{text-align:center;color:#7183a5;font-size:12px;padding:8px 0 20px}footer span{color:#a4b7d6}
@media(max-width:760px){main{width:min(100% - 24px,600px);padding-top:18px}.hero{padding:24px}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.hours{grid-template-columns:repeat(3,minmax(0,1fr))}.days{grid-template-columns:1fr}.day{padding:15px}.temp{letter-spacing:-5px}}@media(max-width:420px){.brand{font-size:19px}.hero-top{align-items:flex-start}.weather-icon{font-size:58px}.live{font-size:10px;padding:7px 9px}.section{padding:17px}.hours{gap:7px}.hour{padding:13px 3px}.hour-temp{font-size:16px}}@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}

/* Smooth premium motion layer */
html{scroll-behavior:smooth}
body{background-size:140% 140%;animation:ambient-shift 34s ease-in-out infinite alternate}
@keyframes ambient-shift{0%{background-position:0% 0%}100%{background-position:100% 70%}}
.search{animation:soft-rise .8s cubic-bezier(.22,1,.36,1) .08s both}
.hero{animation:soft-rise .95s cubic-bezier(.22,1,.36,1) .12s both}
.metrics .metric{animation:soft-rise .8s cubic-bezier(.22,1,.36,1) both}
.metrics .metric:nth-child(1){animation-delay:.18s}
.metrics .metric:nth-child(2){animation-delay:.27s}
.metrics .metric:nth-child(3){animation-delay:.36s}
.metrics .metric:nth-child(4){animation-delay:.45s}
.section:nth-of-type(1){animation:soft-rise .9s cubic-bezier(.22,1,.36,1) .3s both}
.hour{animation:soft-rise .7s cubic-bezier(.22,1,.36,1) both}
.hour:nth-child(1){animation-delay:.22s}.hour:nth-child(2){animation-delay:.28s}
.hour:nth-child(3){animation-delay:.34s}.hour:nth-child(4){animation-delay:.40s}
.hour:nth-child(5){animation-delay:.46s}.hour:nth-child(6){animation-delay:.52s}
.day{animation:soft-rise .75s cubic-bezier(.22,1,.36,1) both}
.day:nth-child(1){animation-delay:.18s}.day:nth-child(2){animation-delay:.3s}.day:nth-child(3){animation-delay:.42s}
@keyframes soft-rise{from{opacity:0;transform:translateY(22px) scale(.99);filter:blur(3px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.metric:hover,.hour:hover,.day:hover{transform:translateY(-5px) scale(1.015);box-shadow:0 16px 35px #0002}
button:active{transform:translateY(0) scale(.97)}
input{transition:border-color .4s ease,box-shadow .4s ease,background .4s ease}
.weather-icon{transform-origin:50% 60%}
.hero:after{animation:halo-breathe 9s ease-in-out infinite alternate}
@keyframes halo-breathe{from{opacity:.45;transform:scale(.92)}to{opacity:1;transform:scale(1.08)}}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  body{animation:none}
  .search,.hero,.metrics .metric,.section:nth-of-type(1),.hour,.day{animation:none}
}

</style>
</head>
<body>
<div class="sky"><i></i><i></i><i></i></div>
<div class="stars"></div>
<main>
<nav>
  <div class="brand"><div class="brandmark">☼</div> atmos<span style="color:#91ecff">.</span></div>
  <div class="live"><span class="dot"></span> LIVE WEATHER</div>
</nav>
<form class="search" method="get" action="/">
  <input name="city" value="{{ city|e }}" placeholder="Search a city — e.g. Mumbai" aria-label="City name" required>
  <button type="submit">Search&nbsp; ↗</button>
</form>
{% if error %}<div class="error">⚠ {{ error }}</div>{% endif %}
{% if weather %}
<section class="glass hero">
  <div class="hero-top">
    <div>
      <div class="eyebrow">Current weather</div>
      <div class="location">{{ city }}, {{ country }}</div>
      <div class="condition">{{ condition }}</div>
    </div>
    <div class="weather-icon">{{ icon }}</div>
  </div>
  <div class="temp-line"><div class="temp">{{ temp|round(1) }}°</div><div style="font-size:22px;color:#b6c7e4">C</div></div>
  <div class="feels">Feels like {{ feels|round(1) }}°C <span style="padding:0 8px;color:#607494">•</span> {{ description }}</div>
  <div class="updated">Updated from weather service · {{ updated }}</div>
</section>
<div class="metrics">
  <div class="glass metric"><div class="metric-icon">💧</div><div class="metric-label">HUMIDITY</div><div class="metric-value">{{ humidity }}%</div></div>
  <div class="glass metric"><div class="metric-icon">🌬️</div><div class="metric-label">WIND SPEED</div><div class="metric-value">{{ wind|round(1) }} <small style="font-size:12px;color:#a9b7d3">km/h</small></div></div>
  <div class="glass metric"><div class="metric-icon">🌧️</div><div class="metric-label">PRECIPITATION</div><div class="metric-value">{{ precipitation|round(1) }} <small style="font-size:12px;color:#a9b7d3">mm</small></div></div>
  <div class="glass metric"><div class="metric-icon">☔</div><div class="metric-label">RAIN CHANCE</div><div class="metric-value">{{ rain_now }}%</div></div>
</div>
<section class="glass section">
  <div class="section-head"><h2>Hourly forecast</h2><div class="section-sub">Next 6 hours</div></div>
  <div class="hours">
  {% for h in hourly %}
    <div class="hour"><div class="hour-time">{{ h.time }}</div><div class="hour-icon">{{ h.icon }}</div><div class="hour-temp">{{ h.temp|round(1) }}°</div><div class="hour-rain">☂ {{ h.rain }}%</div></div>
  {% endfor %}
  </div>
</section>
<section class="glass section">
  <div class="section-head"><h2>3-day outlook</h2><div class="section-sub">Daily forecast</div></div>
  <div class="days">
  {% for d in daily %}
    <div class="day"><div class="day-date">{{ d.date }}</div><div class="day-condition">{{ d.condition }}</div><div class="day-bottom"><div class="day-icon">{{ d.icon }}</div><div class="day-range">{{ d.min|round(0)|int }}° <span style="color:#8495b4">/</span> {{ d.max|round(0)|int }}°C</div></div><div class="day-rain">☂ Rain probability {{ d.rain }}%</div></div>
  {% endfor %}
  </div>
</section>
{% endif %}
<footer>Made with <span>Python + Flask</span> · Weather data by Open-Meteo · Auto-refresh every 5 minutes</footer>
</main>
</body>
</html>
"""

def fetch_json(url, params):
    query = urlencode(params)
    with urlopen(url + "?" + query, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))

def describe(code):
    mapping = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Fog", "🌫️"),
        48: ("Freezing fog", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Drizzle", "🌦️"),
        55: ("Heavy drizzle", "🌧️"),
        56: ("Freezing drizzle", "🌧️"),
        57: ("Freezing drizzle", "🌧️"),
        61: ("Light rain", "🌦️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️"),
        66: ("Freezing rain", "🌧️"),
        67: ("Heavy freezing rain", "🌧️"),
        71: ("Light snow", "🌨️"),
        73: ("Snow", "❄️"),
        75: ("Heavy snow", "❄️"),
        77: ("Snow grains", "🌨️"),
        80: ("Rain showers", "🌦️"),
        81: ("Rain showers", "🌧️"),
        82: ("Heavy showers", "🌧️"),
        85: ("Snow showers", "🌨️"),
        86: ("Heavy snow showers", "❄️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with hail", "⛈️"),
        99: ("Severe thunderstorm", "⛈️"),
    }
    return mapping.get(code, ("Variable conditions", "🌤️"))

def get_weather(city):
    geo = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {"name": city, "count": 1, "language": "en"}
    )
    places = geo.get("results", [])
    if not places:
        raise ValueError("City not found. Check the spelling and try again.")
    place = places[0]
    data = fetch_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "hourly": "temperature_2m,precipitation_probability,weather_code",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": 3,
            "timezone": "auto"
        }
    )
    return place, data

@app.route("/")
def home():
    city = request.args.get("city", "Bhubaneswar").strip() or "Bhubaneswar"
    try:
        place, data = get_weather(city)
        current = data["current"]
        condition, icon = describe(current["weather_code"])
        hourly_data = data["hourly"]
        daily_data = data["daily"]
        start = next(
            (i for i, t in enumerate(hourly_data["time"])
             if t[:13] == current["time"][:13]), 0
        )
        hourly = []
        for i in range(start, min(start + 6, len(hourly_data["time"]))):
            desc, hour_icon = describe(hourly_data["weather_code"][i])
            hourly.append({
                "time": hourly_data["time"][i][11:16],
                "temp": hourly_data["temperature_2m"][i],
                "rain": hourly_data["precipitation_probability"][i],
                "icon": hour_icon
            })
        daily = []
        for i, date in enumerate(daily_data["time"]):
            desc, day_icon = describe(daily_data["weather_code"][i])
            try:
                pretty_date = datetime.strptime(date, "%Y-%m-%d").strftime("%a, %d %b")
            except ValueError:
                pretty_date = date
            daily.append({
                "date": pretty_date,
                "condition": desc,
                "icon": day_icon,
                "min": daily_data["temperature_2m_min"][i],
                "max": daily_data["temperature_2m_max"][i],
                "rain": daily_data["precipitation_probability_max"][i]
            })
        return render_template_string(
            PAGE,
            city=place["name"],
            country=place.get("country", ""),
            temp=current["temperature_2m"],
            feels=current["apparent_temperature"],
            humidity=current["relative_humidity_2m"],
            wind=current["wind_speed_10m"],
            precipitation=current["precipitation"],
            rain_now=hourly_data["precipitation_probability"][start],
            condition=condition,
            description="Live conditions",
            icon=icon,
            updated=current["time"].replace("T", " "),
            hourly=hourly,
            daily=daily,
            weather=True,
            error=""
        )
    except Exception as error:
        return render_template_string(
            PAGE,
            city=city, country="", temp=0, feels=0, humidity=0, wind=0,
            precipitation=0, rain_now=0, condition="", description="",
            icon="🌦️", updated="", hourly=[], daily=[],
            weather=None, error=f"Could not load weather. Check your internet connection and city name. Details: {error}"
        ), 502

if __name__ == "__main__":
    print("Starting Atmos Weather...")
    print("Open http://127.0.0.1:8001 in your browser.")
    app.run(host="127.0.0.1", port=8001, debug=False)
