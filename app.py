import streamlit as st
from weather_utils import get_weather, get_forecast, format_sun_time
import plotly.graph_objs as go


# Set page config
st.set_page_config(layout="wide", page_title="Weather App", page_icon="🌤️")

# Inject custom CSS
st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(135deg, #d1f4f9 0%, #fceabb 100%);
        font-family: 'Segoe UI', sans-serif;
    }

    h1, h2, h3 {
        color: #1e3a8a;
    }

    .stMetric {
        background-color: rgba(255, 255, 255, 0.75);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# Title
st.markdown("<h1 class='title'>🌍 Real-Time Weather App</h1>", unsafe_allow_html=True)

# Input
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("🔍 Enter city name", placeholder="e.g. Mumbai, London, Tokyo")
with col2:
    unit = st.radio("🌡️ Unit", ("Celsius", "Fahrenheit"))
unit_mode = "metric" if unit == "Celsius" else "imperial"

if city:
    weather = get_weather(city, unit_mode)
    if weather.get("cod") != 200:
        st.error("❌ City not found or API error. Please try again.")
    else:
        st.markdown(f"### 📍 Current Weather in **{weather['name']}**")

        # Show metrics
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("🌡️ Temperature", f"{weather['main']['temp']}° {unit[0]}")
        with c2:
            st.metric("💧 Humidity", f"{weather['main']['humidity']}%")
        with c3:
            st.metric("🌬️ Wind Speed", f"{weather['wind']['speed']} m/s")

        col4, col5 = st.columns(2)
        with col4:
            st.success(f"🌅 **Sunrise:** {format_sun_time(weather['sys']['sunrise'], weather['timezone'])}")
        with col5:
            st.info(f"🌇 **Sunset:** {format_sun_time(weather['sys']['sunset'], weather['timezone'])}")

        # Forecast
        st.markdown("### 📈 5-Day Forecast")
        forecast = get_forecast(city, unit_mode)
        temps = []
        times = []
        for entry in forecast['list'][:40:3]:
            temps.append(entry['main']['temp'])
            times.append(entry['dt_txt'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=times, y=temps, mode='lines+markers', name='Temperature', line=dict(color='royalblue')))
        fig.update_layout(title='Temperature Trend', xaxis_title='Time', yaxis_title=f'Temperature (°{unit[0]})')
        st.plotly_chart(fig, use_container_width=True)
