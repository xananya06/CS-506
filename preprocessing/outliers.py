# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %%
#Load the data
DATA_PATH = '../data/'

dataframe = pd.read_csv(DATA_PATH + 'combined_all_employees_salaries_cleaned.csv')
print(dataframe.head())

# %%
#Lets use the IQR strategy to detect the outliers per column
# IQR = Q3 - Q1

# %%
#Calculate the IQR for each column which is a number
for column in dataframe.select_dtypes(include=[np.number]):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    print(f'{column} IQR: {IQR}')

#Plot the percentage outliers per column
# %%
#Calculate the percentage of outliers per column
outliers = []
for column in dataframe.select_dtypes(include=[np.number]):
    if column == 'Year':
        continue
    if column == 'Zip Code':
        continue
    non_zero_values = dataframe[dataframe[column] != 0][column]
    Q1 = non_zero_values.quantile(0.25)
    Q3 = non_zero_values.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers.append(non_zero_values[(non_zero_values < lower_bound) | (non_zero_values > upper_bound)].shape[0] / non_zero_values.shape[0] * 100)

import numpy as np
import matplotlib.pyplot as plt

columns = dataframe[1:].select_dtypes(include=[np.number]).columns[:-2]
colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(columns))) # Using a colormap for distinction

plt.barh(columns, outliers, color=colors)
plt.xlabel('Outlier Percentage')
plt.ylabel('Feature Name')
# Make the title bold
plt.title('Outlier Analysis per Feature (Excluding Zeros)', fontweight='bold')
# plt.gca().invert_yaxis()  # Keeps the order consistent
plt.show()






# %%



