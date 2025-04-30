#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import process
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from scipy.stats import randint

DATA_PATH= "../data"
salaries = pd.read_csv(f"{DATA_PATH}/combined_all_employees_salaries_cleaned.csv")
bpd_salaries =salaries[salaries['Department Name'] == 'Boston Police Department']
bpd_salaries = bpd_salaries[bpd_salaries['Year']==2024] #Change this
roster= pd.read_csv(f"{DATA_PATH}/Responsive_record2020.csv")

#print the number of rows in salaries and roster
print("Number of rows in salaries:", len(bpd_salaries))
print("Number of rows in roster:", len(roster))
#
#If roster['Job Title'] includes 'Police Off', change it to 'Police Officer'
# If 'Job Title' contains 'Police Off', replace it with 'Police Officer'
roster['Job Title'] = roster['Job Title'].apply(
    lambda x: 'Police Officer' if 'Police Off' in str(x) else x
)
roster['Job Title'] = roster['Job Title'].apply(
    lambda x: 'Police Sergeant' if 'Serge' in str(x) else x
)
roster['Job Title'] = roster['Job Title'].apply(
    lambda x: 'Police Lieutenant' if 'Police Lie' in str(x) else x
)
roster['Job Title'] = roster['Job Title'].apply(
    lambda x: 'Police Captain' if 'Capt' in str(x) else x
)
# Step 1: Create a "Name" column in the same format as bpd_salaries
roster['Name'] = roster['Last'].str.strip().str.upper() + ',' + roster['First Name'].str.strip().str.upper()
# Step 2: Merge on Name
merged = roster.merge(
    bpd_salaries[['Name', 'Overtime', 'Total Earnings']],
    on='Name',
    how='left'  # keep all roster entries
)
# See how many missing
missing_matches = merged['Overtime'].isna().sum()
print(f"Number of roster entries with no salary match: {missing_matches}")
print(len(merged))

# List of salary names
salary_names = bpd_salaries['Name'].dropna().unique()

# Function: fuzzy match a name to the closest salary name
def get_best_match(name):
    match, score = process.extractOne(name, salary_names)
    return match if score >= 95 else None  # Only accept good matches (you can lower threshold)

# Apply fuzzy matching
roster['Matched Name'] = roster['Name'].apply(get_best_match)

# See how many got matched
print(f"Number of fuzzy matched names: {roster['Matched Name'].notna().sum()}")
merged_fuzzy = roster.merge(
    bpd_salaries[['Name', 'Overtime', 'Total Earnings']],
    left_on='Matched Name',
    right_on='Name',
    how='left',
    suffixes=('_roster', '_salary')
)

# Drop the extra 'Name_salary' column if you want
merged_fuzzy = merged_fuzzy.drop(columns=['Name_salary'])
missing_matches = merged_fuzzy['Total Earnings'].isna().sum()
print(f"Number of roster entries with no salary match: {missing_matches}")
#Drop those with no match
merged_fuzzy = merged_fuzzy[merged_fuzzy['Overtime'].notna()]
#Check the number of rows
print(len(merged_fuzzy))

sns.set(style="whitegrid")
plt.figure(figsize=(12, 7))
sorted_jobs = merged_fuzzy.groupby('Job Title')['Overtime'].sum().sort_values(ascending=False).index
sns.scatterplot(
    data=merged_fuzzy,
    x='Job Title',
    y='Overtime',
    hue='Job Title',  # Optional, adds color variation by title
    palette='tab20',
    alpha=0.6,
    edgecolor='w',
    linewidth=0.5,
    legend=False
)

plt.title('Overtime Pay by Job Title 2024', fontsize=16, weight='bold')
plt.xlabel('Job Title', fontsize=12)
plt.ylabel('Overtime Pay ($)', fontsize=12)
plt.xticks(rotation=75, ha='right', fontsize=9)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('overtime_by_job_title.png', dpi=300)
plt.show()
# Prepare data
X = pd.get_dummies(merged_fuzzy[['Job Title', 'Sex', 'Ethnic Grp', 'TskProfID']], drop_first=True)
y = merged_fuzzy['Overtime']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Define search space
param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': [None, 10, 20, 30, 40],
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5),
    'max_features': ['auto', 'sqrt', 'log2']
}

# Randomized Search
rf = RandomForestRegressor(random_state=42)
search = RandomizedSearchCV(
    rf,
    param_distributions=param_dist,
    n_iter=30,
    cv=3,
    scoring='neg_mean_absolute_error',  # 👈 this flips the sign
    random_state=42,
    n_jobs=-1,
    verbose=1
)
search.fit(X_train, y_train)

# Best model
best_model = search.best_estimator_
y_pred = best_model.predict(X_test)

print("Best Params:", search.best_params_)
print("MAE:", mean_absolute_error(y_test, y_pred))
# Recompute predictions using best_model
X_full = pd.get_dummies(merged_fuzzy[['Job Title', 'Sex', 'Ethnic Grp', 'TskProfID']], drop_first=True)
predictions = best_model.predict(X_full)
merged_fuzzy['Predicted Overtime'] = np.clip(predictions, a_min=0, a_max=None)

# Group by Job Title
grouped = merged_fuzzy.groupby('Job Title')[['Overtime', 'Predicted Overtime']].mean().reset_index()
grouped = grouped.sort_values('Overtime', ascending=False)
plt.figure(figsize=(14, 6))
sns.barplot(data=grouped.melt(id_vars='Job Title', value_vars=['Overtime', 'Predicted Overtime']),
            x='Job Title', y='value', hue='variable', palette='Set2')

plt.xticks(rotation=45, ha='right')
plt.ylabel("Average Overtime Pay")
plt.title("Actual vs Predicted Average Overtime Pay by Job Title (Tuned RF)")
plt.legend(title="")
plt.tight_layout()
plt.show()

merged_fuzzy['Residual'] = merged_fuzzy['Predicted Overtime'] - merged_fuzzy['Overtime']
# Mean residual by Sex
residual_by_sex = merged_fuzzy.groupby('Sex')['Residual'].mean().reset_index()

# Mean residual by Ethnic Group
residual_by_ethnic = merged_fuzzy.groupby('Ethnic Grp')['Residual'].mean().reset_index()
# Set style
sns.set(style="whitegrid")

# Define a function to annotate bars
def annotate_bars(ax):
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}', 
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=10, color='black', weight='bold')

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Sex residuals
sns.barplot(data=residual_by_sex, x='Sex', y='Residual', palette='RdBu', ax=axes[0])
axes[0].axhline(0, color='black', linestyle='--')
axes[0].set_title("Average Residual by Sex", fontsize=14)
axes[0].set_ylabel("Mean Prediction Error (Predicted - Actual)", fontsize=12)
axes[0].set_xlabel("Sex", fontsize=12)
annotate_bars(axes[0])

# Ethnic Group residuals
sns.barplot(data=residual_by_ethnic, x='Ethnic Grp', y='Residual', palette='RdBu', ax=axes[1])
axes[1].axhline(0, color='black', linestyle='--')
axes[1].set_title("Average Residual by Ethnic Group", fontsize=14)
axes[1].set_xlabel("Ethnic Group", fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
annotate_bars(axes[1])

plt.suptitle("Overtime Prediction Bias by Demographics", fontsize=16, weight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()