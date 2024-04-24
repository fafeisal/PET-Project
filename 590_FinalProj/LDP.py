import numpy as np
import pandas as pd

#add file path
file_path = 'Filtered Glassdoor Gender Pay Gap.csv' 
data = pd.read_csv(file_path)

#test data file 
required_columns = ['JobTitle', 'Gender', 'Age', 'Education', 'BasePay']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"CSV file is missing the following required columns: {', '.join(missing_columns)}")

#privacy parameter  
epsilon = 0.5

# Laplace-distributed noise to each salary
def add_laplace_noise(salaries, epsilon):
    sensitivity = 10000 
    scale = sensitivity / epsilon
    return [salary + np.random.laplace(0, scale) for salary in salaries]

# Group data by gender and apply noise
grouped_data = data.groupby('Gender')['BasePay'].apply(list).to_dict()
noisy_averages = {}

for gender, salaries in grouped_data.items():
    noisy_salaries = add_laplace_noise(salaries, epsilon)
    noisy_average = np.mean(noisy_salaries)
    noisy_averages[gender] = noisy_average

# averages for male/female
for gender, avg in noisy_averages.items():
    print(f"Noisy average BasePay for {gender}: ${avg:.2f}")