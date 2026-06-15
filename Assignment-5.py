# ==============================================================================
# PANDAS ASSIGNMENT SOLUTIONS
# ==============================================================================

import pandas as pd

# 1. Import pandas as pd and read Salaries.csv as a dataframe called sal
sal = pd.read_csv('Salaries.csv')

# 2. Check the head of the DataFrame
print("DataFrame Head:")
print(sal.head())
print("\n" + "="*50 + "\n")

# 3. Use the .info() method to find out how many entries there are
print("DataFrame Info:")
sal.info()
print("\n" + "="*50 + "\n")

# 4. What is the average BasePay?
avg_base_pay = sal['BasePay'].mean()
print(f"Average BasePay: {avg_base_pay}")

# 5. What is the highest amount of OvertimePay in the dataset?
max_overtime_pay = sal['OvertimePay'].max()
print(f"Highest OvertimePay: {max_overtime_pay}")

# 6. What is the job title of JOSEPH DRISCOLL? 
# Note: Use all caps, otherwise you may get an answer that doesn't match up
joseph_job = sal[sal['EmployeeName'] == 'JOSEPH DRISCOLL']['JobTitle'].iloc[0]
print(f"Job title of JOSEPH DRISCOLL: {joseph_job}")

# 7. How much does JOSEPH DRISCOLL make (including benefits)?
joseph_total_pay = sal[sal['EmployeeName'] == 'JOSEPH DRISCOLL']['TotalPayBenefits'].iloc[0]
print(f"Total Pay & Benefits for JOSEPH DRISCOLL: {joseph_total_pay}")

# 8. What is the name of highest paid person (including benefits)?
highest_paid_person = sal[sal['TotalPayBenefits'] == sal['TotalPayBenefits'].max()]
print("\nHighest Paid Person Row Data:")
print(highest_paid_person)
# Alternatively, to get just the name string: highest_paid_person['EmployeeName'].iloc[0]

# 9. What is the name of lowest paid person (including benefits)? 
# Do you notice something strange about how much he or she is paid?
lowest_paid_person = sal[sal['TotalPayBenefits'] == sal['TotalPayBenefits'].min()]
print("\nLowest Paid Person Row Data:")
print(lowest_paid_person)
# Note: The strange observation is that the value is negative (-618.13).

# 10. What was the average (mean) BasePay of all employees per year? (2011-2014)?
avg_base_pay_per_year = sal.groupby('Year')['BasePay'].mean()
print("\nAverage BasePay Per Year:")
print(avg_base_pay_per_year)

# 11. How many unique job titles are there?
unique_jobs_count = sal['JobTitle'].nunique()
print(f"\nNumber of unique job titles: {unique_jobs_count}")

# 12. What are the top 5 most common jobs?
top_5_jobs = sal['JobTitle'].value_counts().head(5)
print("\nTop 5 Most Common Jobs:")
print(top_5_jobs)

# 13. How many Job Titles were represented by only one person in 2013? 
# (e.g. Job Titles with only one occurrence in 2013?)
sal_2013 = sal[sal['Year'] == 2013]
job_counts_2013 = sal_2013['JobTitle'].value_counts()
single_person_jobs_2013 = sum(job_counts_2013 == 1)
print(f"\nJob Titles represented by only one person in 2013: {single_person_jobs_2013}")

