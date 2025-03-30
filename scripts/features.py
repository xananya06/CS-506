import pandas as pd

file_path = "preprocessed_2020.csv"
df = pd.read_csv(file_path)

print("Columns in DataFrame:", df.columns.tolist())

df.columns = df.columns.str.strip()

if 'contact_date' in df.columns:
    df['contact_date'] = pd.to_datetime(df['contact_date'], errors='coerce')

string_columns = [
    'fc_num', 'contact_officer', 'contact_officer_name', 'supervisor',
    'supervisor_name', 'street', 'city', 'state', 'zip', 'stop_duration',
    'circumstance', 'basis', 'vehicle_year', 'vehicle_state', 'vehicle_model',
    'vehicle_color', 'vehicle_style', 'vehicle_type', 'key_situations',
    'contact_reason', 'narrative', 'weather','year'
]

for col in string_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

if 'vehicle_year' in df.columns:
    df['vehicle_year'] = pd.to_numeric(df['vehicle_year'], errors='coerce')

if 'stop_duration' in df.columns:
    df['stop_duration'] = pd.to_numeric(df['stop_duration'], errors='coerce')


if 'contact_date' in df.columns:
    df['day_of_week'] = df['contact_date'].dt.day_name()
    df['time_of_day'] = pd.cut(
        df['contact_date'].dt.hour,
        bins=[0, 6, 12, 18, 24],
        labels=['Night', 'Morning', 'Afternoon', 'Evening'],
        right=False
    )
    df['is_weekend'] = df['contact_date'].dt.dayofweek >= 5
    df['month'] = df['contact_date'].dt.month

if {'vehicle_year', 'vehicle_color', 'vehicle_type'}.issubset(df.columns):
    df['is_vehicle_interaction'] = df[['vehicle_year', 'vehicle_color', 'vehicle_type']].notna().any(axis=1)

if 'stop_duration' in df.columns:
    df['stop_duration_category'] = pd.cut(
        df['stop_duration'],
        bins=[0, 5, 15, 60],
        labels=['Short', 'Medium', 'Long'],
        right=False
    )

if 'supervisor' in df.columns:
    df['supervisor_involved'] = df['supervisor'].notna()

if 'zip' in df.columns:
    df['urban_suburban'] = 'Unknown'  
if 'narrative' in df.columns:
    df['contains_firearm'] = df['narrative'].str.contains('firearm', case=False, na=False)
    df['contains_arrest'] = df['narrative'].str.contains('arrest', case=False, na=False)

if 'contact_officer' in df.columns and 'fc_num' in df.columns:
    officer_contacts = df.groupby('contact_officer')['fc_num'].count().reset_index(name='total_contacts')
    df = df.merge(officer_contacts, on='contact_officer', how='left')

if 'zip' in df.columns and 'fc_num' in df.columns:
    area_contacts = df.groupby('zip')['fc_num'].count().reset_index(name='area_contacts')
    df = df.merge(area_contacts, on='zip', how='left')

if 'key_situations' in df.columns:
    df['high_risk_interaction'] = df['key_situations'].str.contains("Body Worn Camera|Weapon", case=False, na=False)

if 'circumstance' in df.columns:
    df['is_compliant'] = df['circumstance'].str.contains('Stopped', case=False, na=False)

if 'contact_reason' in df.columns:
    df['summons_issued'] = df['contact_reason'].str.contains('Summons', case=False, na=False)
else:
    print("Warning: 'contact_reason' column not found in dataset.")

cleaned_file_path = "2020_features.csv"
df.to_csv(cleaned_file_path, index=False)
print("Feature-engineered data saved to", cleaned_file_path)
