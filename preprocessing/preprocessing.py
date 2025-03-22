# %% [markdown]
# # Preprocessing Data

# %%
#Libraries
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)


# %%
#Load in data
def add_year(df, year):
    df['Year'] = year
    return df

dfs=[]

DATA_PATH = "../data/"
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2011.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2012.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2013.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2014.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2015.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2016.csv", encoding='ISO-8859-1'))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2017.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2018.csv", encoding='ISO-8859-1'))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2019.csv"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2020.csv", encoding='ISO-8859-1'))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2021.csv", encoding='ISO-8859-1'))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2022.csv"))
dfs.append(pd.read_excel(DATA_PATH + "all_employees_2023.xlsx"))
dfs.append(pd.read_csv(DATA_PATH + "all_employees_2024.csv"))

#Still need to add 2024

#Add year to each dataframe
for i in range(len(dfs)):
    dfs[i] = add_year(dfs[i], 2011+i)

# %%
#Print the number of missing values in each dataframe
for i in range(len(dfs)):
    print("Year: " + str(2011+i))
    print(dfs[i].isnull().sum())
    print("\n")
    #Print 2020 dataframe
    # if i == 9:
    #     print(dfs[i].head())
    #     print("\n")

# %%
column_mapping = {
    "NAME": "Name",
    "DEPARTMENT": "Department Name",
    "DEPARTMENT_NAME": "Department Name",
    "DEPARTMENT NAME": "Department Name",
    "TITLE": "Title",
    "REGULAR": "Regular",
    "RETRO": "Retro",
    "OTHER": "Other",
    "OVERTIME": "Overtime",
    "INJURED": "Injured",
    "DETAIL ": "Detail",
    "DETAILS": "Detail",
    "DETAIL": "Detail",
    "QUINN": "Quinn",
    "QUINN/EDUCATION INCENTIVE": "Quinn",
    "QUINN / EDUCATION INCENTIVE": "Quinn",
    "QUINN_EDUCATION": "Quinn",
    "QUINN_EDUCATION_INCENTIVE": "Quinn",
    "TOTAL EARNINGS": "Total Earnings",
    "TOTAL_ GROSS": "Total Earnings",
    "TOTAL_GROSS": "Total Earnings",
    "TOTAL GROSS": "Total Earnings",
    "ZIP": "Zip Code",
    "POSTAL": "Zip Code",
    "ZIP CODE": "Zip Code",
    "Year" : "Year",
    "YEAR"  : "Year"
}

def clean_columns(df):
    df = df.rename(columns=lambda x: x.strip())  
    df = df.rename(columns=str.upper)  
    df = df.rename(columns=column_mapping)  # Apply standardized names
    return df

def clean_salaries(df):
    # Remove dollar signs and commas from salary columns
    salary_columns = ['Total Earnings', 'Regular', 'Retro', 'Other', 'Overtime', 'Injured', 'Detail',
                      'Quinn']
    for col in salary_columns:
        for i in range(len(df[col])):
            if type(df[col][i]) == str:
                df[col][i] = df[col][i].replace("$", "").replace(",", "")
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

    

# Standardize column names for each DataFrame
print("Cleaning columns names...")
dfs = [clean_columns(df) for df in dfs]
print("Done cleaning columns names")

#Print the columns of each dataframe and check if they are the same
for df in dfs:
    # print(df.columns)
    for col in df.columns:
        if col not in dfs[0].columns:
            print("Column", col, "not in first dataframe")

#Clean salaries
print("Cleaning salaries...")
dfs = [clean_salaries(df) for df in dfs]
print("Done cleaning salaries")
        


# %%
#concatenate all the dataframes
df = pd.concat(dfs)


# %%
#Print out all the column types
print(df.dtypes)

# %%
#Save the dataframe to a csv
print("Saving to combined_all_employees_salaries.csv")
df.to_csv("../data/combined_all_employees_salaries.csv", index=False)
print("Saved to combined_all_employees_salaries.csv")


