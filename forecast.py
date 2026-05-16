# ============================================
# NATURAL GAS PRICE FORECASTING PROJECT
# ============================================
# Author : Ritu Mahajan
# Project : Natural Gas Price Prediction
# ============================================

# -----------------------------
# IMPORT LIBRARIES
# -----------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os

# -----------------------------
# CREATE REQUIRED FOLDERS
# -----------------------------

os.makedirs("images", exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------

try:
    df = pd.read_csv("data/Nat_Gas.csv")

except FileNotFoundError:
    print("ERROR: CSV file not found.")
    print("Make sure file exists at:")
    print("data/Nat_Gas.csv")
    exit()

# -----------------------------
# DATA CLEANING
# -----------------------------

# Convert date column
df['Dates'] = pd.to_datetime(df['Dates'])

# Sort values by date
df = df.sort_values('Dates')

# Remove missing values
df = df.dropna()

# Reset index
df = df.reset_index(drop=True)

# -----------------------------
# DISPLAY DATA
# -----------------------------

print("\n===================================")
print("NATURAL GAS DATASET")
print("===================================\n")

print(df.head())

print("\n===================================")
print("DATASET INFORMATION")
print("===================================\n")

print(df.info())

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------

# Convert dates into numeric values
df['Days'] = (
    df['Dates'] - df['Dates'].min()
).dt.days

# Input and output
X = df[['Days']]
y = df['Prices']

# -----------------------------
# TRAIN MACHINE LEARNING MODEL
# -----------------------------

model = LinearRegression()

model.fit(X, y)

# Predictions on training data
y_pred = model.predict(X)

# -----------------------------
# MODEL EVALUATION
# -----------------------------

mse = mean_squared_error(y, y_pred)

r2 = r2_score(y, y_pred)

print("\n===================================")
print("MODEL PERFORMANCE")
print("===================================\n")

print(f"Mean Squared Error : {mse:.2f}")

print(f"R2 Score           : {r2:.2f}")

# -----------------------------
# INTERPOLATION MODEL
# -----------------------------

interp_function = interp1d(
    df['Days'],
    df['Prices'],
    kind='linear',
    fill_value='extrapolate'
)

# -----------------------------
# PRICE ESTIMATION FUNCTION
# -----------------------------

def estimate_price(input_date):

    """
    Estimate natural gas price
    for any given date
    """

    try:

        # Convert input date
        input_date = pd.to_datetime(input_date)

    except:
        return "Invalid date format"

    # Convert date into numeric value
    days = (
        input_date - df['Dates'].min()
    ).days

    # Historical estimation
    if input_date <= df['Dates'].max():

        price = interp_function(days)

    # Future prediction
    else:

        price = model.predict([[days]])[0]

    return round(float(price), 2)

# -----------------------------
# USER INPUT SECTION
# -----------------------------

print("\n===================================")
print("PRICE ESTIMATION")
print("===================================\n")

sample_dates = [
    "2022-06-15",
    "2023-12-25",
    "2025-03-31"
]

for date in sample_dates:

    estimated_price = estimate_price(date)

    print(f"{date}  -->  ${estimated_price}")

# -----------------------------
# HISTORICAL PRICE GRAPH
# -----------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df['Dates'],
    df['Prices'],
    marker='o',
    linewidth=2
)

plt.title(
    "Historical Natural Gas Prices",
    fontsize=16
)

plt.xlabel("Date", fontsize=12)

plt.ylabel("Price", fontsize=12)

plt.grid(True)

# Save graph
plt.savefig(
    "images/historical_prices.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# -----------------------------
# FUTURE FORECASTING
# -----------------------------

future_dates = pd.date_range(
    start=df['Dates'].max(),
    periods=12,
    freq='M'
)

future_days = (
    future_dates - df['Dates'].min()
).days.values.reshape(-1, 1)

future_prices = model.predict(
    future_days
)

# -----------------------------
# FORECAST GRAPH
# -----------------------------

plt.figure(figsize=(14, 6))

# Historical Data
plt.plot(
    df['Dates'],
    df['Prices'],
    label='Historical Prices',
    linewidth=2
)

# Forecast Data
plt.plot(
    future_dates,
    future_prices,
    linestyle='dashed',
    marker='o',
    linewidth=2,
    label='Forecast Prices'
)

plt.title(
    "Natural Gas Price Forecast",
    fontsize=16
)

plt.xlabel("Date", fontsize=12)

plt.ylabel("Price", fontsize=12)

plt.legend()

plt.grid(True)

# Save graph
plt.savefig(
    "images/forecast_prices.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# -----------------------------
# SAVE FUTURE FORECAST CSV
# -----------------------------

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted_Price": np.round(
        future_prices,
        2
    )
})

forecast_df.to_csv(
    "future_forecast.csv",
    index=False
)

# -----------------------------
# FINAL OUTPUT
# -----------------------------

print("\n===================================")
print("PROJECT COMPLETED SUCCESSFULLY")
print("===================================\n")

print("Generated Files:")

print("1. images/historical_prices.png")

print("2. images/forecast_prices.png")

print("3. future_forecast.csv")

print("\nModel is ready for:")
print("- Historical price estimation")
print("- Future forecasting")
print("- Data visualization")

print("\nThank You!")