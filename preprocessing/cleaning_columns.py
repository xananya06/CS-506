# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %%
#Load the data
DATA_PATH = '../data/'

dataframe = pd.read_csv(DATA_PATH + 'combined_all_employees_salaries.csv')
print(dataframe.head())

# %% [markdown]
# # Zip Code
# Convert to format xxxxx, from xxxxx-xxxx and replace Unknown and NaN values with 0. These will be treated as unknown

# %%
#Count the amount of missing values per column relative to the total number of rows per year
print(dataframe.isnull().sum() / len(dataframe))


# %%
#Zip Code
for i in range(0, len(dataframe)):
    if len(str(dataframe.iloc[i]['Zip Code'])) == 4:
        dataframe.at[i, 'Zip Code'] = '0' + str(dataframe.iloc[i]['Zip Code'])
    elif len(str(dataframe.iloc[i]['Zip Code'])) >= 6:
        dataframe.at[i, 'Zip Code'] = str(dataframe.iloc[i]['Zip Code'])[0:5]
    else:
        dataframe.at[i, 'Zip Code'] = str(dataframe.iloc[i]['Zip Code'])

# %%
#Count all the nan values in the dataframe of zip code
print(dataframe['Zip Code'][dataframe['Zip Code']=='nan'].count())
#Make all the nan values in the dataframe of zip code to 0
dataframe['Zip Code'] = dataframe['Zip Code'].replace('nan', '0')

# %%
#Make all the characters in the zip code which are not a number character to 0
dataframe.loc[~dataframe['Zip Code'].str.isnumeric(), 'Zip Code'] = '0'

# %% [markdown]
# # Department Name and Names

# %%
#Remove where department is nan
dataframe = dataframe.dropna(subset=['Department Name'])



# %%
print(dataframe.isnull().sum() / len(dataframe))
#Set all other missing values to 0, because they are all 0
dataframe = dataframe.fillna(0)

# %% [markdown]
# 

# %%
#Save the dataframe to a csv file
dataframe.to_csv(DATA_PATH + 'combined_all_employees_salaries_cleaned.csv', index=False)


