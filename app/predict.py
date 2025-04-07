import joblib
import os
from pathlib import Path

def load_model(model_name):
    """Load a model from the models directory with error handling."""
    try:
        model_path = Path(__file__).parent / 'models' / f'{model_name}.pkl'
        if not model_path.exists():
            print(f"⚠️ Model file not found: {model_path}")
            return None
        return joblib.load(model_path)
    except Exception as e:
        print(f"⚠️ Error loading model {model_name}:", e)
        return None

# Load models with error handling
agri_model = load_model('agri_model')
energy_model = load_model('energy_model')

def predict_agri(temperature, humidity, rainfall, ndvi):
    """Predict agricultural impact based on environmental factors."""
    try:
        if agri_model is None:
            print("⚠️ Agriculture model not loaded")
            return 0.0
            
        # Prepare input data with only the features the model was trained with
        # For agriculture model: temperature, humidity, rainfall
        input_data = [[temperature, humidity, rainfall]]
        
        # Make prediction
        prediction = agri_model.predict(input_data)[0]
        return float(prediction)
    except Exception as e:
        print("⚠️ Error in agricultural prediction:", e)
        return 0.0

def predict_energy(temperature, humidity, rainfall, ndvi):
    """Predict energy usage based on environmental factors."""
    try:
        if energy_model is None:
            print("⚠️ Energy model not loaded")
            return 0.0
            
        # Prepare input data with only the features the model was trained with
        # For energy model: temperature, humidity, rainfall
        input_data = [[temperature, humidity, rainfall]]
        
        # Make prediction
        prediction = energy_model.predict(input_data)[0]
        return float(prediction)
    except Exception as e:
        print("⚠️ Error in energy prediction:", e)
        return 0.0
