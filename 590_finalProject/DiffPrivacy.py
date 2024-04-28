#this script takes in filtered data csv
#utilizes the ibm differential privacy library tools to add noise
#uses the local model laplace mechanism to add noise to each individual salary before calculting averages 
#finds noisy averages for age groups and education levels for males/females 

import numpy as np
import pandas as pd

#ibm's differntial privacy library 
import diffprivlib.tools as dp

#load data 
file_path = 'Filtered Gender Pay Gap.csv'
data = pd.read_csv(file_path)

#test columns
required_columns = ['JobTitle', 'Gender', 'Age', 'Education', 'BasePay']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"CSV file is missing the following columns: {', '.join(missing_columns)}")

#add a income upper bound 
upper_salary_bound = 250000

#apply upper bound to the BasePay column
data['BasePay'] = data['BasePay'].clip(upper=upper_salary_bound)

#privacy parameter
epsilon = 0.59
sensitivity = 10000  

#apply laplce noise mechanism to each individual salary (local model)
scale = sensitivity / epsilon
data['NoisyBasePay'] = data['BasePay'] + np.random.laplace(0, scale, size=len(data))

#calculate the noisy average salary for males/females
for gender in data['Gender'].unique():
    gender_data = data[data['Gender'] == gender]['NoisyBasePay']
    noisy_mean = np.mean(gender_data)
    print(f"Gender: {gender}, Noisy Average BasePay: ${noisy_mean:.2f}")

#finding average noisy income for 2 age groups 
age_groups = {'18-35': (18, 35), '36-65': (36, 65)}
for group_name, (age_min, age_max) in age_groups.items():
    age_group_data = data[(data['Age'] >= age_min) & (data['Age'] <= age_max)]
    dp_means_by_gender = {}
    for gender in age_group_data['Gender'].unique():
        gender_data = age_group_data[age_group_data['Gender'] == gender]['BasePay']
        dp_mean = dp.mean(gender_data, bounds=(0, upper_salary_bound), epsilon=epsilon)
        dp_means_by_gender[gender] = dp_mean
    print(f"Age group {group_name}:")
    for gender, avg in dp_means_by_gender.items():
        print(f"  Noisy average BasePay for {gender}: ${avg:.2f}")

#finding incomes for different education levels and income by gender 
education_levels = ['College', 'Masters', 'PhD']
for education in education_levels:
    edu_data = data[data['Education'] == education]
    dp_means_by_gender = {}
    for gender in edu_data['Gender'].unique():
        gender_data = edu_data[edu_data['Gender'] == gender]['BasePay']
        dp_mean = dp.mean(gender_data, bounds=(0, upper_salary_bound), epsilon=epsilon)
        dp_means_by_gender[gender] = dp_mean
    print(f"Education level {education}:")
    for gender, avg in dp_means_by_gender.items():
        print(f"  Noisy average BasePay for {gender}: ${avg:.2f}")