#this scipt finds the true averages of income data 
#this is done to test the accuracy/privacy trade-off 

import numpy as np
import pandas as pd

file_path = 'Filtered Gender Pay Gap.csv' 
data = pd.read_csv(file_path)

required_columns = ['JobTitle', 'Gender', 'Age', 'Education', 'BasePay']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"CSV file is missing the following required columns: {', '.join(missing_columns)}")

#true average base pay for each gender (average salary for all data)
true_averages = data.groupby('Gender')['BasePay'].mean().to_dict()

# print true averages for male and female
for gender, avg in true_averages.items():
    print(f"True average BasePay for {gender}: ${avg:.2f}")

#averages by age groups 
age_groups = {
    '18-35': (18, 35),
    '36-65': (36, 65)
}
# initialize dictionary to hold results
true_averages_by_age = {}

# loop age group and calc the average base pay for each gender
for group, (age_min, age_max) in age_groups.items():
    filtered_data = data[(data['Age'] >= age_min) & (data['Age'] <= age_max)]
    averages = filtered_data.groupby('Gender')['BasePay'].mean().to_dict()
    true_averages_by_age[group] = averages

# print true averages for each age group and gender
for age_group, averages in true_averages_by_age.items():
    print(f"Age group {age_group}:")
    for gender, avg in averages.items():
        print(f"  True average BasePay for {gender}: ${avg:.2f}")


# education levels 
education_levels = ['College', 'Masters', 'PhD']

# Filter data for the each education levels
filtered_data_by_education = data[data['Education'].isin(education_levels)]

# Calc true average pay for each gender within each given education levels
true_averages_by_education = filtered_data_by_education.groupby(['Gender', 'Education'])['BasePay'].mean().unstack()

# print the results
print("Average BasePay by Gender and Education Level:")
print(true_averages_by_education)