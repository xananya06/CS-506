import pandas as pd
import re
import os

# Get the script's directory and construct the file path
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'fio_final.csv')

# Read the CSV file with low_memory=False to avoid dtype warnings
print("Looking for file at:", file_path)
df = pd.read_csv(file_path, low_memory=False)

# Debug: Check column names
print("Column names:", df.columns.tolist())
print("First few rows:\n", df.head())

# Process the text column (assuming it’s "contact_reason"; adjust if different)
if 'contact_reason' in df.columns:
    df['contact_reason'] = df['contact_reason']  # Already correct, no need to reassign
elif 'U' in df.columns:
    df['contact_reason'] = df['U']
else:
    # Fallback: Assume 21st column (index 20) if no headers match
    print("Assuming 21st column as contact_reason")
    df['contact_reason'] = df.iloc[:, 20]

# Define categories and keywords
categories = [
    ("Drug-Related", ["drug", "narcotics", "controlled substance", "heroin", "cocaine", "marijuana"]),
    ("Traffic Violation", ["traffic stop", "speeding", "red light", "stop sign", "vehicle code", "reckless driving"]),
    ("Suspicious Behavior", ["suspicious", "loitering", "acting strangely", "peeking", "prowling"]),
    ("Theft-Related", ["theft", "shoplifting", "burglary", "stolen", "larceny"]),
    ("Assault-Related", ["assault", "fight", "battery", "violence", "altercation"]),
    ("Robbery", ["robbery", "mugging", "hold-up", "armed robbery"]),
    ("Weapons Violation", ["gun", "knife", "weapon", "firearm", "armed"]),
    ("Warrant Check", ["warrant", "wanted", "fugitive"]),
    ("Disorderly Conduct", ["disorderly", "disturbance", "noise", "drunk", "intoxicated"]),
    ("Trespassing", ["trespass", "intruder", "private property", "unauthorized"]),
    ("Vandalism", ["vandalism", "graffiti", "damage", "deface"]),
    ("Domestic Incident", ["domestic", "family", "spouse", "partner", "abuse"]),
    ("Mental Health", ["mental", "crisis", "unstable", "psychological", "suicidal"]),
    ("Community Interaction", ["community", "resident", "neighborhood", "outreach", "meeting"]),
    ("Response to Call", ["call", "complaint", "911", "report", "emergency"]),
    ("Vehicle Check", ["registration", "inspection", "plate", "vehicle check", "expired tag"]),
    ("Pedestrian Stop", ["pedestrian", "jaywalking", "crossing"]),
    ("Gang Activity", ["gang", "gang-related", "crew", "affiliation"]),
    ("Prostitution", ["prostitution", "soliciting", "escort"]),
    ("Fraud", ["fraud", "scam", "forgery", "counterfeit"]),
    ("General Inquiry", ["inquiry", "questioning", "information", "check"]),
    ("Investigation (Other)", ["investigation", "crime", "incident"]),
    ("Other", [])
]

# Compile regex patterns
patterns = [(cat, [re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE) for kw in kws]) 
            for cat, kws in categories]

# Function to assign a single category
def assign_single_category(text):
    if not isinstance(text, str):
        return "Other"
    for category, regex_list in patterns:
        if category == "Other":
            return category
        for regex in regex_list:
            if regex.search(text):
                return category
    return "Other"

# Apply to DataFrame
df['primary_reason'] = df['contact_reason'].apply(assign_single_category)

# Preview and save (use the actual column name based on debug output)
# Replace 'contact_reason' below with 'U' or the correct name if different
print(df[['contact_reason', 'primary_reason']].head())
df.to_csv(os.path.join(script_dir, 'output_file.csv'), index=False)
print("Processed data saved to output_file.csv")

# import pandas as pd
# import os

# # Assuming the script setup from earlier
# script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'fio_final.csv')

# # Load the CSV
# df = pd.read_csv(file_path, low_memory=False)

# # Find unique cities
# unique_cities = df['city'].unique()
# print("Unique cities in the dataset:", unique_cities)

# # Optionally, count occurrences per city
# city_counts = df['city'].value_counts()
# print("\nCity counts:\n", city_counts)