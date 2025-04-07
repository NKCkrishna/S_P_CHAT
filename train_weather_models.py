import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Step 1: File selection
FILENAME = "daily_weather.parquet"  # Change to your filename if needed

# Step 2: Load data
if FILENAME.endswith('.csv'):
    df = pd.read_csv(f"data/{FILENAME}")
elif FILENAME.endswith('.parquet'):
    df = pd.read_parquet(f"data/{FILENAME}")
else:
    raise ValueError("Unsupported file format")

# Step 3: Display preview
print("📄 Data Preview:")
print(df.head())

# Optional: Drop NaN values
df.dropna(inplace=True)

# Show available columns
print("\n📊 Available Columns:")
print(df.columns)

if FILENAME == "daily_weather.parquet":
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.plot(x='date', y='max_temp_c', kind='line', title="Max Temperature Over Time")
    plt.tight_layout()
    plt.savefig('plots/max_temperature_over_time.png')
    print("📈 Plot saved to plots/max_temperature_over_time.png")

elif FILENAME == "agri_sample.csv":
    sns.barplot(data=df, x='Crop', y='Production')
    plt.title("Crop Production")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/crop_production.png')
    print("📈 Plot saved to plots/crop_production.png")

elif FILENAME == "energy_sample.csv":
    df['Year'] = df['Year'].astype(str)
    sns.lineplot(data=df, x='Year', y='Energy Consumption', hue='Country')
    plt.title("Energy Consumption Over Years")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/energy_consumption.png')
    print("📈 Plot saved to plots/energy_consumption.png")

elif FILENAME == "countries.csv":
    sns.scatterplot(data=df, x='Population', y='GDP')
    plt.title("GDP vs Population")
    plt.tight_layout()
    plt.savefig('plots/gdp_vs_population.png')
    print("📈 Plot saved to plots/gdp_vs_population.png")

elif FILENAME == "cities.csv":
    sns.histplot(data=df, x='Temperature', bins=20)
    plt.title("City Temperature Distribution")
    plt.tight_layout()
    plt.savefig('plots/city_temperature_distribution.png')
    print("📈 Plot saved to plots/city_temperature_distribution.png")

else:
    print("ℹ️ No specific visualization logic found for this file.")
