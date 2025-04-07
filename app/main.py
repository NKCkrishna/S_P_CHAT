import streamlit as st
import pandas as pd
import tempfile
import os
from io import BytesIO
from fpdf import FPDF
from streamlit.components.v1 import html
from weather_api import get_weather
from gee_module import get_ndvi, get_ndvi_image
from utils import suggest_agri, suggest_energy
from predict import predict_agri, predict_energy
from chatbot_api import get_chatbot_response
import sys
from pathlib import Path
import uuid
import time
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Initialize session state for chat
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ─────────────── CONFIG ───────────────
st.set_page_config(page_title="SustainifyAI", layout="wide")

# Toggle Dark Mode
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
st.markdown(
    f"""
    <style>
    body {{
        background-color: {'#0e1117' if dark_mode else '#ffffff'};
        color: {'#ffffff' if dark_mode else '#000000'};
    }}
    .card {{
        background-color: {'#1f2937' if dark_mode else '#f3f4f6'};
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }}
    .chat-message {{
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }}
    .chat-message.user {{
        background-color: {'#1f2937' if dark_mode else '#f3f4f6'};
    }}
    .chat-message.assistant {{
        background-color: {'#374151' if dark_mode else '#e5e7eb'};
    }}
    .chat-message .avatar {{
        width: 40px;
        height: 40px;
        margin-right: 1rem;
        border-radius: 50%;
    }}
    .chat-message .content {{
        flex-grow: 1;
    }}
    .typing-indicator {{
        display: flex;
        align-items: center;
        margin: 1rem 0;
    }}
    .typing-indicator span {{
        height: 8px;
        width: 8px;
        margin: 0 2px;
        background-color: {'#ffffff' if dark_mode else '#000000'};
        border-radius: 50%;
        display: inline-block;
        animation: typing 1s infinite;
    }}
    .typing-indicator span:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    .typing-indicator span:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    @keyframes typing {{
        0% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
        100% {{ transform: translateY(0); }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ─────────────── SIDEBAR NAVIGATION ───────────────
page = st.sidebar.radio("Navigation", ["Dashboard", "Chatbot"])

if page == "Dashboard":
    st.title(":seedling: SustainifyAI Dashboard")
    st.markdown("Smart insights for agriculture, energy, and the environment.")

    # ────────────── CITY SELECTION ──────────────
    city = st.text_input("🔍 Enter City", value="Delhi")
    city = city.title().strip()

    # Default coordinates with fallback
    default_coords = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Bangalore": (12.9716, 77.5946)
    }

    # Dynamic location using geopy if not predefined
    if city in default_coords:
        lat, lon = default_coords[city]
    else:
        try:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="sustainify")
            location = geolocator.geocode(city)
            if location:
                lat, lon = location.latitude, location.longitude
            else:
                st.error("❌ Could not locate city. Using Delhi as fallback.")
                lat, lon = default_coords["Delhi"]
        except Exception as e:
            st.error(f"❌ Error in geocoding: {str(e)}. Using Delhi as fallback.")
            lat, lon = default_coords["Delhi"]

    # ────────────── DATA FETCH ──────────────
    try:
        weather = get_weather(city)
        ndvi = get_ndvi(lat, lon)
        ndvi_map_html = get_ndvi_image(lat, lon)
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        weather = {"temp": 25, "humidity": 50, "rain": 0}
        ndvi = 0.0
        ndvi_map_html = None

    # ────────────── GOOGLE MAP ──────────────
    st.subheader("📍 City Location Map")
    st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

    # ────────────── INTERACTIVE SLIDERS ──────────────
    st.subheader("⚙️ Customize Environmental Factors")

    temp_slider = st.slider("Temperature (°C)", 0, 50, int(weather['temp']))
    humidity_slider = st.slider("Humidity (%)", 0, 100, int(weather['humidity']))
    rainfall_slider = st.slider("Rainfall (mm)", 0, 300, int(weather['rain']))
    ndvi_value = st.slider("NDVI", -1.0, 1.0, float(round(ndvi, 2)), step=0.01)
    energy_slider = st.slider("⚡ Energy Usage (kWh)", 0, 100, 50)

    # ────────────── CARDS UI ──────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="card"><h3>🌡 Temp</h3><p>{temp_slider}°C</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="card"><h3>💧 Humidity</h3><p>{humidity_slider}%</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="card"><h3>🌧 Rainfall</h3><p>{rainfall_slider} mm</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="card"><h3>🌱 NDVI</h3><p>{round(ndvi_value, 2)}</p></div>""", unsafe_allow_html=True)

    # ────────────── PDF REPORT DOWNLOAD ──────────────
    def generate_pdf(temp, humidity, rain, ndvi_val):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SustainifyAI Report", ln=True, align="C")
            pdf.cell(200, 10, txt=f"City: {city}", ln=True)
            pdf.cell(200, 10, txt=f"Temperature: {temp}°C", ln=True)
            pdf.cell(200, 10, txt=f"Humidity: {humidity}%", ln=True)
            pdf.cell(200, 10, txt=f"Rainfall: {rain} mm", ln=True)
            pdf.cell(200, 10, txt=f"NDVI: {round(ndvi_val, 2)}", ln=True)

            # Create a temporary file to save the PDF
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            try:
                pdf.output(temp_file.name)
                with open(temp_file.name, 'rb') as f:
                    pdf_data = f.read()
                return pdf_data
            finally:
                temp_file.close()
                try:
                    os.unlink(temp_file.name)
                except:
                    pass  # Ignore deletion errors
        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            return None

    pdf_data = generate_pdf(temp_slider, humidity_slider, rainfall_slider, ndvi_value)
    if pdf_data:
        st.download_button("🗅 Download PDF Report", data=pdf_data, file_name="SustainifyAI_Report.pdf", mime="application/pdf")

    # ────────────── SUSTAINABILITY SCORE ──────────────
    st.subheader("♻️ Final Sustainability Score")
    if st.button("🔍 Check Sustainability"):
        try:
            score = 100
            score -= abs(temp_slider - 25) * 0.4
            score -= abs(humidity_slider - 50) * 0.3
            score -= abs(rainfall_slider - 100) * 0.2
            score += max(-1, min(1, ndvi_value)) * 25
            score -= energy_slider * 0.2
            score = max(0, min(100, round(score)))
            st.success(f"Overall Sustainability Score: {score}/100")
        except Exception as e:
            st.error(f"❌ Error calculating sustainability score: {str(e)}")

    # ────────────── PREDICTIONS ──────────────
    st.subheader("📊 Predictions")
    try:
        agri_pred = predict_agri(temp_slider, humidity_slider, rainfall_slider, ndvi_value)
        energy_pred = predict_energy(temp_slider, humidity_slider, rainfall_slider, ndvi_value)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="card"><h3>🌾 Agriculture</h3><p>{suggest_agri(agri_pred)}</p></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="card"><h3>⚡ Energy</h3><p>{suggest_energy(energy_pred)}</p></div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error generating predictions: {str(e)}")

else:  # Chatbot page
    st.title("🤖 SustainifyAI Assistant")
    st.markdown("Chat with our AI assistant about sustainability, agriculture, and energy.")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about sustainability..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get chatbot response without context
        try:
            response = get_chatbot_response(prompt)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            # Add error message to chat history
            st.session_state.messages.append({"role": "assistant", "content": "I apologize, but I encountered an error. Please try again."})
            with st.chat_message("assistant"):
                st.write("I apologize, but I encountered an error. Please try again.")

    # Add clear chat button
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
