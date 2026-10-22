
import requests
import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="SkyCast | Weather",
    page_icon="🌤️",
    layout="wide"
)

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #0b1225, #111d38 55%, #172b49);
    color: #f8fafc;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label {
    color: #f8fafc;
}
.hero {
    background: linear-gradient(120deg, #2563eb, #06b6d4);
    padding: 30px;
    border-radius: 24px;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px #00000030;
}
.hero h1 {
    font-size: 38px;
    margin: 0;
    color: white;
}
.hero p {
    color: #e0f2fe;
    margin-bottom: 0;
}
.metric-card {
    background: linear-gradient(145deg, #1c2b49, #17243d);
    border: 1px solid #344767;
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 8px 20px #00000020;
}
.metric-label {
    color: #a8bad5;
    font-size: 14px;
}
.metric-value {
    color: white;
    font-size: 27px;
    font-weight: 700;
    margin-top: 12px;
}
.weather-panel {
    background: linear-gradient(135deg, #243b64, #182943);
    border: 1px solid #40567a;
    border-radius: 22px;
    padding: 28px;
    margin: 18px 0;
}
.big-temp {
    font-size: 64px;
    font-weight: 750;
    color: white;
    line-height: 1.2;
}
.muted {
    color: #b5c6df;
}
.forecast-card {
    background: #1a2944;
    border: 1px solid #344767;
    border-radius: 16px;
    padding: 15px 8px;
    text-align: center;
    min-height: 145px;
}
div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #0891b2);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    min-height: 45px;
}
div.stButton > button:hover {
    border: 1px solid #67e8f9;
    color: white;
}
div[data-testid="stTextInput"] input {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- WEATHER HELPERS ----------------
WEATHER_CODES = {
    0: ("☀️", "Clear sky"),
    1: ("🌤️", "Mainly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"),
    48: ("🌫️", "Rime fog"),
    51: ("🌦️", "Light drizzle"),
    53: ("🌦️", "Drizzle"),
    55: ("🌧️", "Heavy drizzle"),
    61: ("🌧️", "Light rain"),
    63: ("🌧️", "Moderate rain"),
    65: ("🌧️", "Heavy rain"),
    71: ("🌨️", "Light snow"),
    73: ("❄️", "Snow"),
    75: ("❄️", "Heavy snow"),
    80: ("🌦️", "Rain showers"),
    81: ("🌧️", "Moderate showers"),
    82: ("⛈️", "Heavy showers"),
    95: ("⛈️", "Thunderstorm"),
    96: ("⛈️", "Thunderstorm with hail"),
    99: ("⛈️", "Severe thunderstorm")
}


def get_city(name):
    response = requests.get(
        GEO_URL,
        params={
            "name": name,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=15
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return results[0] if results else None


def get_weather(latitude, longitude):
    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "precipitation,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),
            "forecast_days": 5,
            "timezone": "auto"
        },
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def metric_card(label, value, emoji):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{emoji} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- DASHBOARD HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🌤️ SkyCast</h1>
    <p>Your world, your weather. Live conditions and a
    five-day forecast in one place.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- CITY SEARCH ----------------
with st.form("weather_search"):
    city_name = st.text_input(
        "📍 Search a city",
        placeholder="Try Bhubaneswar, Mumbai, London..."
    )
    submitted = st.form_submit_button(
        "🔍 Get Weather",
        use_container_width=True
    )

# Keep the last successful result visible after interactions.
if submitted:
    if not city_name.strip():
        st.session_state.pop("weather_result", None)
        st.warning("Please enter a city name.")
    else:
        try:
            with st.spinner("Getting the latest weather data..."):
                location = get_city(city_name.strip())

                if location is None:
                    st.session_state.pop("weather_result", None)
                    st.error("City not found. Check the spelling.")
                else:
                    data = get_weather(
                        location["latitude"],
                        location["longitude"]
                    )
                    st.session_state["weather_result"] = {
                        "location": location,
                        "data": data
                    }

        except requests.exceptions.RequestException:
            st.error(
                "Could not connect to the weather service. "
                "Check your internet and try again."
            )

# ---------------- DISPLAY WEATHER ----------------
result = st.session_state.get("weather_result")

if result:
    location = result["location"]
    weather = result["data"]
    current = weather["current"]
    daily = weather["daily"]

    code = current["weather_code"]
    icon, description = WEATHER_CODES.get(
        code, ("🌡️", "Weather conditions unavailable")
    )

    st.markdown(
        f"### 📍 {location['name']}, "
        f"{location.get('admin1') or location.get('country', '')}"
    )
    st.markdown(
        f'<p class="muted">Local weather data time: '
        f'{current["time"].replace("T", " ")}</p>',
        unsafe_allow_html=True
    )

    # Main conditions panel
    left, right = st.columns([1.3, 1])

    with left:
        st.markdown(f"""
        <div class="weather-panel">
            <div style="font-size:58px">{icon}</div>
            <div class="muted">CURRENT WEATHER</div>
            <div class="big-temp">{current['temperature_2m']}°C</div>
            <h3>{description}</h3>
            <p class="muted">Feels like
            {current['apparent_temperature']}°C</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("#### 🌍 Weather at a glance")
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">'
            f'💧 Humidity</div><div class="metric-value">'
            f'{current["relative_humidity_2m"]}%</div></div>',
            unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">'
            f'💨 Wind speed</div><div class="metric-value">'
            f'{current["wind_speed_10m"]} km/h</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("### 📊 Weather details")

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Feels like",
            f'{current["apparent_temperature"]}°C',
            "🌡️"
        )
    with c2:
        metric_card(
            "Precipitation",
            f'{current["precipitation"]} mm',
            "🌧️"
        )
    with c3:
        metric_card(
            "Humidity",
            f'{current["relative_humidity_2m"]}%',
            "💧"
        )

    # Five-day forecast
    st.markdown("### 🗓️ Five-day forecast")

    columns = st.columns(5)

    for i, column in enumerate(columns):
        forecast_code = daily["weather_code"][i]
        forecast_icon, forecast_description = WEATHER_CODES.get(
            forecast_code, ("🌡️", "Unknown")
        )

        day = daily["time"][i]
        rain = daily["precipitation_probability_max"][i]
        rain_text = f"{rain}%" if rain is not None else "N/A"

        with column:
            st.markdown(f"""
            <div class="forecast-card">
                <div class="muted">{day}</div>
                <div style="font-size:34px;margin:10px 0">
                    {forecast_icon}
                </div>
                <div style="font-size:12px">{forecast_description}</div>
                <div style="margin-top:10px;font-weight:700">
                    {daily['temperature_2m_max'][i]}°
                    / {daily['temperature_2m_min'][i]}°
                </div>
                <div class="muted" style="font-size:12px">
                    🌧️ {rain_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Temperature chart
    st.markdown("### 📈 Temperature trends")

    chart_data = pd.DataFrame({
        "Date": daily["time"],
        "Maximum temperature": daily["temperature_2m_max"],
        "Minimum temperature": daily["temperature_2m_min"]
    }).set_index("Date")

    st.line_chart(chart_data)

    st.caption(
        "Data: Open-Meteo. Weather values are model-based "
        "estimates and forecasts, not guaranteed local observations."
    )

else:
    st.markdown("""
    <div class="weather-panel" style="text-align:center">
        <div style="font-size:60px">🌎</div>
        <h3>Your forecast starts here</h3>
        <p class="muted">Search for a city above to explore its
        current conditions and five-day forecast.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center;color:#8fa5c4;'
    'margin-top:40px">Built with Python · Streamlit · Open-Meteo</p>',
    unsafe_allow_html=True
)
