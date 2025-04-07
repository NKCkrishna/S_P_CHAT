# 🌿 SustainifyAI

SustainifyAI is a smart, AI-powered sustainability dashboard that provides real-time insights into agriculture, energy usage, and environmental health. It integrates live weather data, NDVI-based vegetation indices, and a sustainability scoring engine to help individuals, farmers, and policymakers make data-driven decisions for a greener future.

## 🚀 Features

- 🔍 **City-Based Search** with smart geolocation
- 🌤 **Real-Time Weather**: Temperature, humidity, and rainfall from OpenWeather API
- 🌱 **NDVI Insights**: Google Earth Engine-powered vegetation health analysis
- 🗺 **Google Map View**: Instantly locate the selected city on a map
- 📊 **Interactive Sliders**: Customize environmental conditions
- 📦 **Card-Based Dashboard UI**: A clean overview of key metrics
- 🧮 **Sustainability Score**: A calculated score based on environmental inputs
- 🖼 **NDVI Heatmap**: Image or map visualization of vegetation index
- 🧾 **Downloadable PDF Report**: Export and share city-specific sustainability reports
- 🌙 **Dark Mode Toggle** for better user experience
- 🔮 **Upcoming**: Agriculture & Energy prediction models

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Weather API**: [OpenWeatherMap](https://openweathermap.org/)
- **NDVI Data**: Google Earth Engine
- **PDF Generation**: [FPDF](https://py-pdf.github.io/fpdf2/)
- **Geolocation**: [Geopy](https://github.com/geopy/geopy)

## 📦 Installation

```bash
git clone https://github.com/your-username/SustainifyAI.git
cd SustainifyAI
pip install -r requirements.txt
streamlit run app/main.py


SustainifyAI/
│
├── app/
│   ├── main.py               # Streamlit dashboard
│   ├── utils.py              # Utilities (score, suggestions)
│   ├── weather_api.py        # Weather API handler
│   ├── gee_module.py         # NDVI + GEE integration
│   ├── predict.py            # Future: ML predictions
│
├── assets/                   # Optional: store logos/images
├── requirements.txt
└── README.md
