#this script adds some test data to the original data to test how much income averages will be impacted with new data 

import numpy as np
import pandas as pd

def add_laplace_noise_to_salary(salary, epsilon):
    sensitivity = 10000  
    scale = sensitivity / epsilon
    return salary + np.random.laplace(0, scale)

def main():
    file_path = 'Filtered Gender Pay Gap.csv'
    data = pd.read_csv(file_path)

    #test columns
    required_columns = ['JobTitle', 'Gender', 'Age', 'Education', 'BasePay']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"CSV file is missing the following required columns: {', '.join(missing_columns)}")

    #upper salary bound
    upper_salary_bound = 200000  
    data['BasePay'] = data['BasePay'].clip(upper=upper_salary_bound)

    #adding random test to income data
    np.random.seed(42)
    test_salaries = np.random.randint(50000, 200000, size=10)
    test_genders = np.random.choice(['Male', 'Female'], size=10)
    test_ages = np.random.randint(18, 65, size=10)
    test_education = np.random.choice(['College', 'Masters', 'PhD'], size=10)

    test_data = pd.DataFrame({
        'JobTitle': ['TestJob' for _ in range(10)],
        'Gender': test_genders,
        'Age': test_ages,
        'Education': test_education,
        'BasePay': test_salaries
    })

    #concat test data to the original data
    combined_data = pd.concat([data, test_data], ignore_index=True)

    #apply dp to the combined data
    epsilon = 0.55
    combined_data['NoisyBasePay'] = combined_data['BasePay'].apply(lambda x: add_laplace_noise_to_salary(x, epsilon))

    #analyze &  print results
    noisy_averages = combined_data.groupby('Gender')['NoisyBasePay'].mean().to_dict()
    for gender, avg in noisy_averages.items():
        print(f"Noisy average BasePay for {gender} with test data: ${avg:.2f}")

if __name__ == "__main__":
    main()
