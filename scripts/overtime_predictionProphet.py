#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from prophet import Prophet
import itertools

DATA_PATH= "../data"
salaries = pd.read_csv(f"{DATA_PATH}/combined_all_employees_salaries_cleaned.csv")
print(salaries.head())

#Prophet

# Prepare splits
train_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] <= 2021)]
val_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] >= 2022) & (salaries['Year'] <= 2023)]
test_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] == 2024)]

# Aggeregate
def aggregate(df):
    df = df.groupby('Year')['Overtime'].sum().reset_index()
    df = df.rename(columns={'Year': 'ds', 'Overtime': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], format='%Y')
    return df

train_df = aggregate(train_df)
val_df = aggregate(val_df)
test_df = aggregate(test_df)

# Hyperparameters
param_grid = {
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
    'seasonality_mode': ['additive', 'multiplicative']
}

# Generate all combinations of parameters
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]

best_val_mae = float('inf')
best_params = None
best_model = None

# Validation dates
future_val = pd.date_range(start='2022-01-01', end='2023-01-01', freq='YS')
future_val = pd.DataFrame({'ds': future_val})

#Run Prophet with hyperparameter tuning
for params in all_params:
    m = Prophet(
        interval_width=0.95,
        changepoint_prior_scale=params['changepoint_prior_scale'],
        seasonality_prior_scale=params['seasonality_prior_scale'],
        seasonality_mode=params['seasonality_mode']
    )
    m.fit(train_df)
    
    forecast_val = m.predict(future_val)
    val_merged = val_df.merge(forecast_val[['ds', 'yhat']], on='ds', how='left')
    val_mae = mean_absolute_error(val_merged['y'], val_merged['yhat'])
    
    if val_mae < best_val_mae:
        best_val_mae = val_mae
        best_params = params
        best_model = m

print(f"Best validation MAE: ${best_val_mae:,.2f}")
print(f"Best Parameters: {best_params}")

# Evaluate on test set
future_test = pd.date_range(start='2024-01-01', end='2024-01-01', freq='YS')
future_test = pd.DataFrame({'ds': future_test})

forecast_test = best_model.predict(future_test)
test_merged = test_df.merge(forecast_test[['ds', 'yhat']], on='ds', how='left')
test_mae = mean_absolute_error(test_merged['y'], test_merged['yhat'])

print(f"Test MAE (2024): ${test_mae:,.2f}")

# Forecast 2025
future_2025 = pd.DataFrame({'ds': pd.to_datetime(['2025-01-01'])})
forecast_2025 = best_model.predict(future_2025)

print("\nForecasted Overtime for 2025:")
print(f"  2025: ${forecast_2025['yhat'].iloc[0]:,.2f}")

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(train_df['ds'], train_df['y'] / 1_000_000, 'o-', label='Train', markersize=6)
future_val_predict = best_model.predict(future_val)
val_merged = val_df.merge(future_val_predict[['ds', 'yhat']], on='ds', how='left')
ax.plot(val_df['ds'], val_df['y'] / 1_000_000, 'o', color='green', label='Validation Actual')
ax.plot(val_merged['ds'], val_merged['yhat'] / 1_000_000, 'x', color='green', label='Validation Prediction')
ax.plot(test_df['ds'], test_df['y'] / 1_000_000, 'o', color='red', label='Test Actual')
ax.plot(test_merged['ds'], test_merged['yhat'] / 1_000_000, 'x', color='red', label='Test Prediction')
ax.plot(forecast_2025['ds'], forecast_2025['yhat'] / 1_000_000, 'd', color='blue', label='Forecast 2025', markersize=8)
future_full = pd.date_range(start='2010-01-01', end='2025-01-01', freq='YS')
future_full_df = pd.DataFrame({'ds': future_full})
forecast_full = best_model.predict(future_full_df)
ax.plot(forecast_full['ds'], forecast_full['yhat'] / 1_000_000,
        linestyle='--',
        color='black',
        linewidth=2,
        label='Prophet Forecast Line')
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title('BPD Overtime Forecast (Prophet with Hyperparameter Tuning)', fontsize=16, fontweight='bold')
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('Total Overtime ($ Millions)', fontsize=13)
ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)
ax.legend(frameon=True, fontsize=11)
plt.tight_layout()
plt.show()

