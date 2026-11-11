#Small Project 1 Ela I.


#Question 0 Set Up the Data
#Import numpy
import numpy as np
#Import csv since will use for data
import csv 
#Read in data for students names and instruments
students ="names.csv"
with open(students, 'r') as dat:
  for line in csv.DictReader(dat):
      print(line)
#Read in data for students names and sales/donations
sales ="sales.csv"
with open(sales, 'r') as dat2:
  for line2 in csv.DictReader(dat2):
      print(line2)
      
      
#Question 1 How Many Bags of Popcorn did the Band Sell?
#Turn data into a list
with open(sales, 'r') as dat2:
    data = list(csv.DictReader(dat2))
#Make empty lists for values
bags_popcorn=[]
donations = []
#Function to run through code and count bags of popcorn
def sum_popcorn(data):
#Start at zero
    total = 0
    for row in data:
#Go to sale part of the dictionary list
        if 'sale' in row:
            sale_value = row['sale'].strip()
#Remove the dollar sign and convert to float for later
            if sale_value.startswith('$'):
                donation = int(sale_value[1:])
#Donations list to turn into array later
                donations.append(donation)
            else: 
                try:
#Split the number from the "bags of popcorn text"
                    num_bags = int(row['sale'].split()[0])
#Bags of popcorn list to turn into array later
                    bags_popcorn.append(num_bags)     
#Add up and total
                    total += num_bags
#Skip over when it is sale in dollars for donations
                except ValueError:
                    continue
    return total
#Print the outputs
result = sum_popcorn(data)
    #print(bags_popcorn)
    #print(donations)
print(result, "bags of popcorn were sold.")


#Question 2 How Well did they do at Fundraising?
#a. Average sale
#$3/bag
popcorn_price=3
#Turn lists into arrays
bags_array = np.array(bags_popcorn)
donations_array=np.array(donations)
    #print(bags_array)
    #print(donations_array)
#Find the mean and multiply to find the average
add = np.sum(bags_array)
avg=np.divide(add, 50)
profit=np.multiply(avg, popcorn_price)
#Print outputs
print(f"Average sale: ${profit:.2f}")

#b. Average donation
add2=np.sum(donations_array)
avg2=np.divide(add2, 50)
print(f"Average donations: ${avg2:.2f}")

#c. Total amount raised from popcorn sales
add2=np.sum(bags_array)
total_sales=np.multiply(add2, popcorn_price)
print(f"Total popcorn profit: ${total_sales:.2f}")

#d. Total amount raised from donations
total_donations=np.sum(donations_array)
print(f"Total donations: ${total_donations:.2f}")

#e. Total amount raised
total=np.add(total_sales, total_donations)
print(f"Total raised: ${total:.2f}")


#Question 3 What is the total, average, max, and min sales by instruemnt?
#10 instruments, 50 students for array. total amount of donations and bags on popcorn
#Create a 2D numpy matrix 
# Read students data again (names and instruments) 
students_data = {}
with open('names.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        students_data[row['student']] = row['instrument']
# Read sales data again
sales_data = {}
with open('sales.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['student']
        sale = row['sale']
#Getting rid of $ and adding the numbers as integers
        if sale.startswith('$'):
            donation = int(float(sale[1:]))
#Comparing whether it is sale or donation
            if name not in sales_data:
                sales_data[name] = {'donation': donation, 'popcorn': 0}
            else:
#Add donations together as is
                sales_data[name]['donation'] += donation
        else:
#Add the amount of popcorns as is
            popcorn = int(sale.split()[0])
            if name not in sales_data:
                sales_data[name] = {'donation': 0, 'popcorn': popcorn}
            else:
                sales_data[name]['popcorn'] += popcorn
# Get list of instruments
instruments = sorted(list(set(students_data.values())))
# Create dictionary to map instruments to columns
instrument_index = {instrument: i for i, instrument in enumerate(instruments)}
# Create empty matrix
matrix = np.zeros((len(students_data), len(instruments)), dtype=int)
# Fill matrix with values from above 
for i, (name, instrument) in enumerate(students_data.items()):
    col_index = instrument_index[instrument]
#Multiply popcorn bags by 3 to get the amount that goes to the band
    popcorn_value = sales_data[name]['popcorn'] * 3  
    donation_value = sales_data[name]['donation']
#Add all the values for the total
    total_value = popcorn_value + donation_value
    matrix[i, col_index] = total_value
# Print the matrix
#print(matrix)
#Refrence to see if right
#print("\nRows Students:")
#for i, name in enumerate(students_data.keys()):
    #print(f"{i}: {name}")
#print("\nColumns Instruments - Total Value:")
#for i, instrument in enumerate(instruments):
    #print(f"{i}: {instrument}")
#Finding total amount raised
total = np.sum(matrix, axis=0)
#Finding average sales per student
#avg = np.divide(total, 50) #If looking for specific value of each kid including those not in that instrument group
#Make an empty list
column_avg = []
#Compare each value and do not count for the average the zeros, while counting the number of students
for col in range(matrix.shape[1]):
    non_zeros = matrix[:, col][matrix[:, col] != 0]
    avg = np.mean(non_zeros) if len(non_zeros) > 0 else 0
    column_avg.append(avg)
column_avg = np.array(column_avg).tolist()
#Finding highest individual sale
max_sale = np.max(matrix, axis=0)
#Finding lowest individual sale
min_sale = np.min(matrix, axis=0) #If including the people that didn't donate
column_min = np.min(np.where(matrix != 0, matrix, np.inf), axis=0)
#Output and print in the correct format
print("Sales by Instrument:")
for i, instrument in enumerate(instruments):
    print(f"{instrument.capitalize()}: Total: ${total[i]:.2f} | Avg: ${column_avg[i]:.2f} per student | Max: ${max_sale[i]:.2f} | Min: ${column_min[i]:.2f}")


#Question 4 Who raised the most money for each instrument?
#Find the max and then connected with the student that is the top earner
max_sale = np.max(matrix, axis=0)
top_earners = np.argmax(matrix, axis=0)
#Make an empty list of the student names to be able to pull from
names = list(students_data.keys())
#Output and print in the correct format
print("Top Fundraisers by Instrument:")
for i, instrument in enumerate(instruments):
    top = names[top_earners[i]]
    num = max_sale[i]
    print(f"{instrument.capitalize()}: {top} - ${num:.2f}")


#Question 5 Which instrument has the highest proportion of donation vs popcorn sales?
#Same matrix code from above (Question 3)
students_data = {}
with open('names.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        students_data[row['student']] = row['instrument']
sales_data = {}
with open('sales.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['student']
        sale = row['sale']
        if sale.startswith('$'):
            donation = int(float(sale[1:]))
            if name not in sales_data:
                sales_data[name] = {'donation': donation, 'popcorn': 0}
            else:
                sales_data[name]['donation'] += donation
        else:
            popcorn = int(sale.split()[0])
            if name not in sales_data:
                sales_data[name] = {'donation': 0, 'popcorn': popcorn}
            else:
                sales_data[name]['popcorn'] += popcorn
instruments = sorted(list(set(students_data.values())))
instrument_index = {instrument: i for i, instrument in enumerate(instruments)}
#This time, need to create an empty matrix for donations and popcorn sales each
donation_matrix = np.zeros((len(students_data), len(instruments)), dtype=int)
popcorn_matrix = np.zeros((len(students_data), len(instruments)), dtype=int)
#Fill matrices with values
for i, (name, instrument) in enumerate(students_data.items()):
    col_index = instrument_index[instrument]
    popcorn_value = sales_data[name]['popcorn'] * 3
    donation_value = sales_data[name]['donation']
    donation_matrix[i, col_index] = donation_value
    popcorn_matrix[i, col_index] = popcorn_value
#Print the matrices
#print(donation_matrix)
#print(popcorn_matrix)
#Calculate the proportions (donation sales/popcorn sales)
column_sums1 = np.sum(donation_matrix, axis=0)
column_sums2 = np.sum(popcorn_matrix, axis=0)
result = np.divide(column_sums1, column_sums2)
#print(result)
#Sort the output in descending order
sorted_proportions = sorted(zip(instruments, result), key=lambda x: x[1], reverse=True)
# Print the results
print("Instrument with highest donation/popcorn proportion:")
for instrument, proportion in sorted_proportions:
    print(f"{instrument}: {proportion:.1f}")