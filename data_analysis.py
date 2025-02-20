import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
try:
    df = pd.read_csv('Seattle_Rescue_Plan.csv')
except FileNotFoundError:
    print("Error: File 'Seattle_Rescue_Plan.csv' not found.")
    exit()

# Clean numeric columns (remove commas, convert to float)
numeric_cols = ['Budgeted', 'Expenditures', 'Encumbrances', 'Total Spent']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].replace('[\$,]', '', regex=True), errors='coerce')

# Handle missing values
df['Encumbrances'].fillna(0, inplace=True)
df.fillna({'Program Status': 'Unknown'}, inplace=True)

# Summary statistics
total_budget = df['Budgeted'].sum()
total_spent = df['Total Spent'].sum()
print(f"Total Budget: ${total_budget:,.2f}")
print(f"Total Spent: ${total_spent:,.2f}")
print(f"Remaining Funds: ${total_budget - total_spent:,.2f}")

# Utilization rate
df['Utilization Rate'] = df['Total Spent'] / df['Budgeted'].replace(0, pd.NA)
df['Utilization Rate'].fillna(0, inplace=True)

# Top budgeted programs
top_budget = df.sort_values('Budgeted', ascending=False).head(10)
print(top_budget[['Program ID', 'Item Name for the Public', 'Budgeted']])

# Pie chart for program status
status_counts = df['Program Status'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
plt.title('Program Status Distribution')
plt.show()

# Budget allocation by program status
plt.figure(figsize=(10, 6))
budget_by_status = df.groupby('Program Status')['Budgeted'].sum().reset_index()
sns.barplot(data=budget_by_status, x='Program Status', y='Budgeted')
plt.xticks(rotation=45)
plt.title('Budget Allocation by Program Status')
plt.show()

# Top departments by budget
dept_budget = df.groupby('Dept (Full Name)')['Budgeted'].sum().sort_values(ascending=False).head(5)
dept_budget.plot(kind='bar', title='Top Departments by Budget')
plt.show()

# Department expenditure efficiency
dept_efficiency = df.groupby('Dept (Full Name)').apply(lambda x: x['Total Spent'].sum() / x['Budgeted'].sum()).replace([float('inf'), pd.NA], 0)
dept_efficiency.sort_values(ascending=False).plot(kind='barh', title='Department Expenditure Efficiency')
plt.show()

# Top 5 funding sources
funding_source = df['Funding Source'].value_counts().head(5)
funding_source.plot(kind='pie', autopct='%1.1f%%', title='Top 5 Funding Sources')
plt.show()

# Budget by investment category
plt.figure(figsize=(10, 6))
category_budget = df.groupby('Category of Investment')['Budgeted'].sum()
category_budget.plot(kind='barh', title='Budget by Investment Category')
plt.show()

# Budget vs. Total Spent by Department
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='Budgeted', y='Total Spent', hue='Dept (Full Name)', size='Utilization Rate', sizes=(20, 200))
plt.title('Budget vs. Total Spent by Department')
plt.show()
