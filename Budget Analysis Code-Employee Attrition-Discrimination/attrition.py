import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
rng = np.random.default_rng(42)
df=pd.read_csv('combined_all_employees_salaries_cleaned.csv')
df=df[df["Department Name"]=="Boston Police Department"]
columns = df.columns.tolist()

df.fillna({'Regular': 0, 'Retro': 0, 'Other': 0, 'Overtime': 0, 'Injured': 0,
           'Detail': 0, 'Quinn': 0, 'Total Earnings': 0}, inplace=True)
df['Zip Code'] = df['Zip Code'].fillna('Unknown')
df['Title'] = df['Title'].fillna('Unknown')


# Infer attrition (1 = left, 0 = stayed)
def inferAttrition(df):
    df = df.sort_values(['Name', 'Year'])
    df['Next_Year'] = df.groupby('Name')['Year'].shift(-1)
    df['Attrition'] = np.where(df['Next_Year'].isna() & (df['Year'] < df['Year'].max()), 1, 0)
    return df


df = inferAttrition(df)

# Lets add new features
df['First_Year'] = df.groupby('Name')['Year'].transform('min')
df['totalYears'] = df['Year'] - df['First_Year']

df["prevOvertime"] = df.groupby('Name')['Overtime'].shift(1)
df["overtimeChange"] = df['Overtime'] - df['prevOvertime']
df["overtimeChange"] = df['overtimeChange'].fillna(0)

# Rolling Average (Hopefully it adds new context)
df['overtimeRolling'] = df.groupby('Name')['Overtime'].rolling(window=3, min_periods=1).mean().reset_index(level=0,
                                                                                                           drop=True)
df['avgOvertime'] = df['overtimeRolling'].fillna(df['Overtime'])

earningsCols = ['Regular', 'Overtime', 'Injured', 'Detail', 'Quinn', 'Total Earnings']
for col in earningsCols:
    df[col] = df[col].clip(lower=0)

# Log-transform earnings
for col in earningsCols:
    df[f'Log_{col}'] = np.log1p(df[col])

dept = LabelEncoder()
title = LabelEncoder()
zip = LabelEncoder()
df['deptEncoded'] = dept.fit_transform(df['Department Name'])
df['titleEncoded'] = title.fit_transform(df['Title'])
df['zipEncoded'] = zip.fit_transform(df['Zip Code'])

features = ['Log_Regular', 'Log_Overtime', 'Log_Injured', 'Log_Detail', 'Log_Quinn',
            'Log_Total Earnings', 'totalYears', 'overtimeChange',
            'avgOvertime', 'deptEncoded', 'titleEncoded', 'zipEncoded']
target = 'Attrition'

# Filter out rows where Year is max (no next year to determine attrition)
df_model = df[df['Year'] < df['Year'].max()].copy()

trainYears = list(range(2011, 2021))
valYears = [2021, 2022]
testYear = 2023

trainDf = df_model[df_model['Year'].isin(trainYears)]
valDf = df_model[df_model['Year'].isin(valYears)]
testDf = df_model[df_model['Year'] == testYear]

X_train = trainDf[features]
y_train = trainDf[target]
X_val = valDf[features]
y_val = valDf[target]
X_test = testDf[features]
y_test = testDf[target]

models = {
    'Logistic Regression': Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=5000))
    ]),
    'Random Forest': Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('classifier', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42))
    ]),
    'XGBoost': Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('classifier', xgb.XGBClassifier(
            scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),
            random_state=42
        ))
    ])
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    proba = model.predict_proba(X_val)[:, 1]
    valPrecision = precision_score(y_val, preds, zero_division=0)
    valRecall = recall_score(y_val, preds, zero_division=0)
    valRoc = roc_auc_score(y_val, proba)

    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    testPrecision = precision_score(y_test, preds, zero_division=0)
    testRecall = recall_score(y_test, preds, zero_division=0)
    testRoc = roc_auc_score(y_test, proba)

    results.append({
        'Model': name,
        'Val Precision': valPrecision,
        'Val Recall': valRecall,
        'Val ROC-AUC': valRoc,
        'Test Precision': testPrecision,
        'Test Recall': testRecall,
        'Test ROC-AUC': testRoc
    })

resultsDf = pd.DataFrame(results)
print("\nModel Performance:\n")
print(resultsDf)

bestModel = models['Random Forest']

X_test_transformed = bestModel.named_steps['imputer'].transform(X_test)
X_test_transformed = pd.DataFrame(X_test_transformed, columns=features)

explainer = shap.TreeExplainer(bestModel.named_steps['classifier'], X_test_transformed)
shap_values = explainer(X_test_transformed)

# Plot SHAP summary for class 1 (attrition)
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values[:, :, 1], X_test_transformed, feature_names=features, show=False, rng=rng)
plt.title('SHAP Feature Importance for Attrition Risk')
plt.tight_layout()
plt.savefig('shapImportance.png')
plt.close()
# Random Forest Feature Importance
rf_classifier = bestModel.named_steps['classifier']
rf_importance = rf_classifier.feature_importances_
importance_df = pd.DataFrame({'Feature': features, 'Importance': rf_importance})
importance_df = importance_df.sort_values('Importance', ascending=False)

# Plot Random Forest feature importance
plt.figure(figsize=(10, 6))
sns.barplot(data=importance_df, x='Importance', y='Feature')
plt.title('Random Forest Feature Importance (Mean Decrease in Impurity)')
plt.tight_layout()
plt.savefig('rf_feature_importance.png')
plt.close()
print("\nRandom Forest Feature Importance:")
print(importance_df)

# Train on all data (Lets goo!)
df_all = df_model[df_model['Year'] <= 2023].copy()
X_all = df_all[features]
y_all = df_all[target]

bestModel.fit(X_all, y_all)

# Lets predict for the next year (Take 2024 and predict the attrition which says if the employee stays or leaves!)
df_pred = df[df['Year'] == 2024].copy()
X_pred = df_pred[features]
pred_probs = bestModel.predict_proba(X_pred)[:, 1]

# Create output dataframe
output = df_pred[['Name', 'Department Name', 'Title', 'Year']].copy()
output['attritionProbability'] = pred_probs
output['attritionRisk'] = np.where(pred_probs > 0.3, 'High', 'Low')

output = output.sort_values('attritionProbability', ascending=False)

output.to_csv('attritionPredictions_2025.csv', index=False)

# Print top 10 at-risk employees
print("\nTop 10 Employees at Risk of Attrition in 2025:\n")
print(output.head(10)[['Name', 'Department Name', 'Title', 'attritionProbability']])

# Summary statistics
print("\nAttrition Risk Summary:")
print(output['attritionRisk'].value_counts(normalize=True))
