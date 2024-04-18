import pandas as pd
import numpy as np

# income range [income_min, income_max]
income_min = 20000
income_max = 300000
count = 1000  # assuming 1000 entries; 

def add_laplace_noise(data, epsilon):
    sensitivity = (income_max - income_min) / count
    noise = np.random.laplace(0, sensitivity / epsilon, 1)
    return data + noise

def calculate_differentially_private_average(data, gender, job_titles, epsilon):
    # Filter data based on gender and job title
    filtered_data = data[(data['Gender'] == gender) & (data['JobTitle'].isin(job_titles))]
    
    # Calculate the true average income
    true_average = filtered_data['BasePay'].mean()
    
    # Adding Laplace noise to the average for differential privacy
    dp_average = add_laplace_noise(true_average, epsilon)
    
    return dp_average

# Load dataset
file_path = 'Filtered Glassdoor Gender Pay Gap.csv'  
data = pd.read_csv(file_path)

#privacy budget (epsilon)
epsilon = 0.1  # Smaller epsilon means more privacy

# Job titles considered
job_titles = ['Data Scientist', 'Financial Analyst', 'IT', 'Software Engineer']

# Calc differentially private average for males
male_dp_average = calculate_differentially_private_average(data, 'Male', job_titles, epsilon)
print(f"Differentially private average income for males: {male_dp_average}")

# Calculate differentially private average for females
female_dp_average = calculate_differentially_private_average(data, 'Female', job_titles, epsilon)
print(f"Differentially private average income for females: {female_dp_average}")