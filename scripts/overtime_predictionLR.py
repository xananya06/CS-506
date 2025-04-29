#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

DATA_PATH= "../data"
salaries = pd.read_csv(f"{DATA_PATH}/combined_all_employees_salaries_cleaned.csv")
print(salaries.head())

#Linear Regression

#Splits
train_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] <= 2021)]
val_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] >= 2022) & (salaries['Year'] <= 2023)]
test_df = salaries[(salaries['Department Name'] == 'Boston Police Department') & (salaries['Year'] == 2024)]

# Aggregate overtime per year
def aggregate(df):
    df = df.groupby('Year')['Overtime'].sum().reset_index()
    df = df.rename(columns={'Year': 'ds', 'Overtime': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], format='%Y')
    return df

train_df = aggregate(train_df)
val_df = aggregate(val_df)
test_df = aggregate(test_df)

# Train on Training data
train_X = train_df['ds'].dt.year.values.reshape(-1, 1)
train_y = train_df['y'].values

lr = LinearRegression()
lr.fit(train_X, train_y)

# Validatiom
val_X = val_df['ds'].dt.year.values.reshape(-1, 1)
val_preds = lr.predict(val_X)

# Test
test_X = test_df['ds'].dt.year.values.reshape(-1, 1)
test_preds = lr.predict(test_X)

# Evaluate
val_mae = mean_absolute_error(val_df['y'], val_preds)
test_mae = mean_absolute_error(test_df['y'], test_preds)

print(f"Validation MAE (2022–2023): ${val_mae:,.2f}")
print(f"Test MAE (2024): ${test_mae:,.2f}")

# Forecast 2025
future_years = np.array([2025]).reshape(-1, 1)
future_dates = pd.to_datetime(future_years.flatten(), format='%Y')
future_preds = lr.predict(future_years)

print("\nForecasted Overtime for 2025:")
for year, pred in zip([2025], future_preds):
    print(f"  {year}: ${pred:,.2f}")

#Plotting
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(train_df['ds'], train_df['y'] / 1_000_000, 'o-', label='Train', markersize=6)
ax.plot(val_df['ds'], val_df['y'] / 1_000_000, 'o', color='green', label='Validation Actual')
ax.plot(val_df['ds'], val_preds / 1_000_000, 'x', color='green', label='Validation Prediction')
ax.plot(test_df['ds'], test_df['y'] / 1_000_000, 'o', color='red', label='Test Actual')
ax.plot(test_df['ds'], test_preds / 1_000_000, 'x', color='red', label='Test Prediction')
ax.plot(future_dates, future_preds / 1_000_000, 'd', color='blue', label='Forecast 2025', markersize=8)
all_years = np.arange(2010, 2026).reshape(-1, 1)
all_dates = pd.to_datetime(all_years.flatten(), format='%Y')
all_preds = lr.predict(all_years)
ax.plot(all_dates, all_preds / 1_000_000,
        linestyle='--',
        color='black',
        linewidth=2,
        label='Linear Regression Line')

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title('BPD Overtime Forecast (Linear Regression)', fontsize=16, fontweight='bold')
ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('Total Overtime ($ Millions)', fontsize=13)
ax.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)
ax.legend(frameon=True, fontsize=11)
plt.tight_layout()
plt.show()