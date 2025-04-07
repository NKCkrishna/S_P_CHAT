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

A Streamlit application for sustainable agriculture and energy management.

## Deployment Instructions

### Prerequisites
1. A GitHub account
2. A Streamlit Cloud account (https://streamlit.io/cloud)
3. Google Earth Engine account
4. Google Gemini API key

### Deployment Steps

1. **Fork this repository** to your GitHub account.

2. **Set up Streamlit Cloud**:
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Connect your GitHub repository
   - Set the main file path to `app/main.py`
   - Add the following secrets in the Streamlit Cloud dashboard:
     - `GEMINI_API_KEY`: Your Google Gemini API key
     - `GEE_EMAIL`: Your Google Earth Engine email
     - `GEE_PROJECT`: Your Google Earth Engine project name

3. **Deploy the application**:
   - Click "Deploy"
   - Wait for the deployment to complete

4. **Access your application**:
   - Once deployed, you'll receive a URL to access your application
   - Share this URL with others to use your application

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/SustainifyAI.git
   cd SustainifyAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file with your API keys
   - Or use the `.streamlit/secrets.toml` file

4. Run the application:
   ```bash
   streamlit run app/main.py
   ```

## Features

- Weather data analysis
- NDVI (Normalized Difference Vegetation Index) mapping
- Agricultural suggestions
- Energy management recommendations
- AI-powered chatbot for sustainability queries

## License

MIT License

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
