#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing


DATA_PATH= "../data"
salaries = pd.read_csv(f"{DATA_PATH}/combined_all_employees_salaries_cleaned.csv")
print(salaries.head())

#HW

# Splits
train_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] <= 2021)]
val_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] >= 2022) & (salaries['Year'] <= 2023)]
test_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] == 2024)]

# Aggregation
def aggregate(df):
    df = df.groupby('Year')['Overtime'].sum().reset_index()
    df = df.rename(columns={'Year': 'ds', 'Overtime': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], format='%Y')
    df = df.set_index('ds')
    return df

train_df = aggregate(train_df)
val_df = aggregate(val_df)
test_df = aggregate(test_df)

# HW train
holt = ExponentialSmoothing(
    train_df['y'],
    trend="add",
    seasonal=None,
    initialization_method="estimated"
)
holt_fit = holt.fit()

# Validation
val_preds = holt_fit.forecast(steps=2)

# Test
test_pred = holt_fit.forecast(steps=3).iloc[-1]  # 3 steps ahead from 2021, 2022, 2023, 2024

# Evaluate
val_mae = mean_absolute_error(val_df['y'], val_preds)
test_mae = mean_absolute_error(test_df['y'], [test_pred])

print(f"Validation MAE (2022–2023): ${val_mae:,.2f}")
print(f"Test MAE (2024): ${test_mae:,.2f}")

# Predict 2025
future_forecast = holt_fit.forecast(steps=4).iloc[-1]  # 4 steps ahead to get 2025
print(f"\nForecasted Overtime for 2025: ${future_forecast:,.2f}")

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(train_df.index, train_df['y'] / 1_000_000, 'o-', label='Train', markersize=6)
ax.plot(val_df.index, val_df['y'] / 1_000_000, 'o', color='green', label='Validation Actual')
ax.plot(val_df.index, val_preds.values / 1_000_000, 'x', color='green', label='Validation Prediction')
ax.plot(test_df.index, test_df['y'] / 1_000_000, 'o', color='red', label='Test Actual')
ax.plot(test_df.index, [test_pred / 1_000_000], 'x', color='red', label='Test Prediction')
future_date = pd.to_datetime('2025', format='%Y')
ax.plot(future_date, future_forecast / 1_000_000, 'd', color='blue', label='Forecast 2025', markersize=8)
fitted_full = pd.concat([
    holt_fit.fittedvalues,
    holt_fit.forecast(steps=4)  # Forecast 2022–2025
])
ax.plot(fitted_full.index, fitted_full.values / 1_000_000,
        linestyle='--',
        color='black',
        linewidth=2,
        label='Holt-Winters Line')
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title('BPD Overtime Forecast (Holt-Winters)', fontsize=16, fontweight='bold')
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('Total Overtime ($ Millions)', fontsize=13)
ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)
ax.legend(frameon=True, fontsize=11)
plt.tight_layout()
plt.show()
