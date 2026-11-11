#Import necessay modules
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#Read in data
sales=pd.read_csv("US_Regional_Sales_Data.csv")
df = pd.DataFrame(sales)

#Clean up data
#Create functions to run through all the data
def dateformat(date):
#Getting rid of the /
    day, month, year = map(int, date.split('/'))
#For all the years that are represented as just 18, 19, 20, adding 2000 will make it in the format YYYY
    if year < 2000:
        year+= 2000
    return f'{year}-{month}'
def getyear(date):
#Seperate the data with a -, for the desired format
    year, month = map(int, date.split('-'))
    return year
#Change the OrderDate column to newly formated YYYY-MM
df['OrderDate'] = df['OrderDate'].apply(dateformat)

#1. Plot 1: Total sales per year by sales channel
#Add a new column for just the years, to easily get the info
df['Year'] = df['OrderDate'].apply(getyear)
df['Total Sale'] = df['Total Sale'].str.replace(',', '', regex=True)
df['Total Sale'] = df['Total Sale'].astype(float).round(2)
#Total sales per year
total_per_year = df.groupby('Year')['Total Sale'].sum()
print(total_per_year)
#Group by year and sales channel
sales_by_channel = df.groupby(['Year', 'Sales Channel'])['Total Sale'].sum().reset_index()
#Pivot
sales_pivot = sales_by_channel.pivot(index='Year', columns='Sales Channel', values='Total Sale')
#Plot
sales_pivot.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis')
#Aesthetics
plt.title('Total Sales Per Year by Sales Channel')
plt.xlabel('Year')
plt.ylabel('Total Sales (USD)')
plt.xticks(rotation=0)
plt.legend(title='Sales Channel', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='-', alpha=0.8)
plt.tight_layout()
#Display
plt.show()

#2. Plot 2: Sales Channel Proportions by Regional Warehouse Per Year
#Group by regional warehouse, yearly sales, sales channel
channel_year_warehouse = df.groupby(['Year', 'RegionalWarehouseCode', 'Sales Channel'])['Total Sale'].sum().reset_index()
#Total sales per wareshouse in the year
total_warehouse_by_year = channel_year_warehouse.groupby(['Year', 'RegionalWarehouseCode'])['Total Sale'].transform('sum')
#Make proportions
channel_year_warehouse['Proportion'] = channel_year_warehouse['Total Sale'] / total_warehouse_by_year
#Pivot and plot
pivot_prop = channel_year_warehouse.pivot_table(index=['Year', 'RegionalWarehouseCode'],columns='Sales Channel', values='Proportion')
pivot_prop.plot(kind='bar', stacked=False, figsize=(14, 7), colormap='rainbow', edgecolor='black', width=0.9)
#Aesthetics
plt.title('Sales Channel Proportions by Regional Warehouse Per Year')
plt.xlabel('Year, Regional Warehouse')
plt.ylabel('Proportion of Sales')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Sales Channel', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
#Display
plt.show()

#3. Plot 3: Sales Teams Annual Performance
#Group by sales team by year
sales_by_team_year = df.groupby(['SalesTeamID', 'Year'])['Total Sale'].sum().reset_index()
sns.set(style="whitegrid")
#Plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=sales_by_team_year, x='SalesTeamID', y='Total Sale', hue='Year', marker='o')
#Aesthetics
plt.title('Total Sales by Sales Team Over the Years')
plt.xlabel('Sales Team ID')
ID = sorted(df['SalesTeamID'].unique())
plt.xticks(ticks=ID)
plt.ylabel('Total Sales')
plt.legend(title='Year')
plt.tight_layout()
#Display
plt.show()

# Plot 4: Stores Specific Total Sales for the 2019 and 2020
#Get rid of 2018
filtered_df = df[df['Year'] != 2018]
#Top stores
top_stores = (filtered_df.groupby(['Year', 'StoreID'])['Total Sale'].sum().reset_index())
#Top in 2019
top10_2019 = top_stores[top_stores['Year'] == 2019].nlargest(10, 'Total Sale')
#Top in 2020
top10_2020 = top_stores[top_stores['Year'] == 2020].nlargest(10, 'Total Sale')
#Checking overlap between the years and stores
overlap = set(top10_2019['StoreID']) & set(top10_2020['StoreID'])
overlap
#Filter the data
top = pd.concat([top10_2019, top10_2020])['StoreID'].unique()
plot_df = filtered_df[filtered_df['StoreID'].isin(top)]
pivot_df = plot_df.pivot_table(values='Total Sale', index='StoreID', columns='Year', aggfunc='sum')
#Plot
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_df, annot=True, fmt=".0f", cmap='Purples', linewidths=0.5)
#Aesthetics
plt.title('Total Sales Heatmap (Top Stores, 2019 & 2020)', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Store ID')
plt.tight_layout()
#Display
plt.show()

