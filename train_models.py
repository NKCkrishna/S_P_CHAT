# train_models.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from joblib import dump

# Train agri model
agri = pd.read_csv('data/agri_sample.csv')
X_agri = agri[['temperature', 'humidity', 'soil_moisture']]
y_agri = agri['rainfall']
model_agri = RandomForestRegressor().fit(X_agri, y_agri)
dump(model_agri, 'models/agri_model.pkl')

# Train energy model
energy = pd.read_csv('data/energy_sample.csv')
X_energy = energy[['hour', 'temp', 'past_usage']]
y_energy = energy['past_usage']
model_energy = RandomForestRegressor().fit(X_energy, y_energy)
dump(model_energy, 'models/energy_model.pkl')
