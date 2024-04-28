#this script filters out the oringinal data csv file to only consider tech job titles
#it drops unecessary columns 
#saves into a new filtered csv file 


import pandas as pd

def filter_file(input_file_path, output_file_path):
    
    data = pd.read_csv(input_file_path)

    job_titles = ['Data Scientist', 'Financial Analyst', 'IT', 'Software Engineer']
    genders = ['Male', 'Female']
    age_range = range(18, 66)  #Age 18 to 65 inclusive
    educations = ['College', 'Masters', 'PhD']
    
    filtered_data = data[
        data['JobTitle'].isin(job_titles) &
        data['Gender'].isin(genders) &
        data['Age'].between(age_range.start, age_range.stop - 1) &
        data['Education'].isin(educations)
    ]
    
    filtered_data = filtered_data.drop(columns=['Bonus']) 
    filtered_data = filtered_data.drop(columns=['Seniority']) 
    filtered_data = filtered_data.drop(columns=['Dept'])
    filtered_data = filtered_data.drop(columns=['PerfEval'])
   
    
    filtered_data.to_csv(output_file_path, index=False)
    print(f"Filtered data saved to {output_file_path}")

#path to input/output file (local file path)


input_file_path = '/Users/mariamrafique/Desktop/590_finalProject/Glassdoor Gender Pay Gap.csv'  
output_file_path = '/Users/mariamrafique/Desktop/590_finalProject/Filtered Gender Pay Gap.csv'  

#run filter_file function 
filter_file(input_file_path, output_file_path)