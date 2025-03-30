import pandas as pd
import numpy as np

file_path = "output_file_final.csv"

df = pd.read_csv(file_path)

print("Initial data shape:", df.shape)
print("Columns:", df.columns.tolist())

# df['year'] = 2024 

df['contact_date'] = pd.to_datetime(df['contact_date'], errors='coerce')


missing_values = df.isnull().sum()
print("Missing values per column:\n", missing_values)

df['vehicle_year'] = pd.to_numeric(df['vehicle_year'], errors='coerce')



string_columns = [
    'fc_num', 'contact_date', 'contact_officer', 'contact_officer_name', 'supervisor',
    'supervisor_name', 'street', 'city', 'state', 'zip', 'stop_duration', 'circumstance',
    'basis', 'vehicle_year', 'vehicle_state', 'vehicle_model', 'vehicle_color', 'vehicle_style',
    'vehicle_type', 'key_situations', 'contact_reason', 'weather', 'stop_duration_category',
    'day_of_week', 'time_of_day', 'month','year', 'primary_reason'
]

for col in string_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()



print("after preprocessing:", df.shape)
print("Unique values in 'circumstance':", df['circumstance'].unique())

cleaned_file_path = "outttt.csv"
df.to_csv(cleaned_file_path, index=False)
print("Cleaned data saved to", cleaned_file_path)

