import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'output_file.csv')
df = pd.read_csv(file_path, low_memory=False)

df['city'] = df['city'].str.upper().fillna('UNKNOWN')  

city_corrections = {
    'BOSOTN': 'BOSTON',
    'E BOSTON': 'EAST BOSTON',
    'S BOSTON': 'SOUTH BOSTON',
    'SOUTHBOSTON': 'SOUTH BOSTON',
    'JAMAICA PL': 'JAMAICA PLAIN',
    'CITY OF BOSTON': 'BOSTON',
    'ROXBURY CROSSING': 'ROXBURY',
    'TOWN OF BROOKLINE': 'BROOKLINE',
    'TOWN OF MILTON': 'MILTON',
    'TOWN OF WINCHESTER': 'WINCHESTER'
}
df['city'] = df['city'].replace(city_corrections)

urban_cities = [
    'BOSTON', 'DORCHESTER', 'ROXBURY', 'JAMAICA PLAIN', 'EAST BOSTON',
    'MATTAPAN', 'SOUTH BOSTON', 'BRIGHTON', 'HYDE PARK', 'CHARLESTOWN',
    'ROSLINDALE', 'WEST ROXBURY', 'ALLSTON'
]

suburban_cities = [
    'QUINCY', 'CAMBRIDGE', 'NEWTON', 'BROOKLINE', 'MILTON', 'ARLINGTON',
    'MALDEN', 'PEABODY', 'DEDHAM', 'LYNN', 'BROCKTON', 'SOMERVILLE',
    'WALTHAM', 'SALEM', 'WALPOLE', 'WINCHESTER', 'EVERETT', 'REVERE',
    'STONEHAM', 'MARSHFIELD', 'RANDOLPH', 'NEEDHAM', 'WATERTOWN',
    'PROVIDENCE', 'TAUNTON', 'CHESTNUT HILL', 'KEARNY', 'ANDOVER',
    'WOBURN', 'NORFOLK', 'WEST SPRINGFIELD', 'LOWELL'
]

def classify_area(city):
    if city in urban_cities:
        return 'urban'
    elif city in suburban_cities:
        return 'suburban'
    else:
        return 'unknown'  
df['urban_suburban'] = df['city'].apply(classify_area)

print(df[['city', 'urban_suburban']].head(10))
print("\nValue counts for urban_suburban:\n", df['urban_suburban'].value_counts())

output_path = os.path.join(script_dir, 'output_file_final.csv')
df.to_csv(output_path, index=False)
print(f"Updated data saved to {output_path}")