#Small Project 2
#Ela Ilic

#Import necessary modules
import pandas as pd
import csv

#1.Average valence per year, written as CSV file 
#Valence=level of happiness a track has
#Read in the file using pd to make it organized
spotify=pd.read_csv("1980sClassics.csv")
df = pd.DataFrame(spotify)
#Take the average of valence grouping by the year
mean_by_year= df.groupby('Year')['Valence'].mean()
#Format as required and print the output
#print(mean_by_year)
#Format the header
header = ['Year', 'Average valence']
#Check if outputs properly
#for year, valence in mean_by_year.items():
    #print(f"{year}, {valence:.5f}")
#Write as csv file
with open('avg_valence_per_year.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
#Get the header from above
    writer.writerow(header)
#Write the output year and corresponding average valence
    for year, valence in mean_by_year.items():
        writer.writerow([year, f"{valence:.5f}"])


#2.Duration of track relate to danceability
#Convert mins:secs to just seconds
#Create a function to change the format
def convert_to_seconds(time_str):
    mins, secs = map(int, time_str.split(':'))
#Multiple the minutes by 60 and add the remaining seconds to find the total seconds
    return mins * 60 + secs
#Apply the function
df['Duration_secs'] = df['Duration'].apply(convert_to_seconds)
#Print and check
#print(df)
#Categorize numerical values into discrete bins => use pd.cut()
#Define the bins and labels
bins = [0, 60, 180, 300, float('inf')]
labels = ['<1 min', '1-3 min', '3-5 min', '>5 min']
#Format and use pd.cut and the bins and labels to sort the seconds into the categories
df['Duration_categories'] = pd.cut(df['Duration_secs'], bins=bins, labels=labels, right=False)
#Print and check
#print(df)
#Get the danceability for songs, choosing only top 5 based on the duration categories
top_danceable_songs = df.groupby('Duration_categories', group_keys=False).apply(
    lambda x: x.nlargest(5, 'Danceability'))
#Print in the correct format and check if correct
#for category in labels:
    #print(f"\nThe category of duration ({category}):")
    #subset = top_danceable_songs[top_danceable_songs['Duration_categories'] == category]
#Set so the outputs are as instructed
    #for _, row in subset.iterrows():
        #print(f"Track: {row['Track']}, Artist: {row['Artist']}, Duration (seconds): {row['Duration_secs']}, Danceability: {row['Danceability']}")
#Write as csv file
with open('top_5_danceability.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
#Get the header from above
    for category in labels:
        writer.writerow([f"The category of duration ({category}):"])
#Organize by categories
        subset = top_danceable_songs[top_danceable_songs['Duration_categories'] == category]
#Change above code so format is correctly outtputed in the csv
        writer.writerow(['Track', 'Artist', 'Duration (seconds)', 'Danceability'])
        for _, row in subset.iterrows():
            writer.writerow([row['Track'], row['Artist'], row['Duration_secs'], row['Danceability']])


#3.Comparing whether high tempo songs are more popular
#Find the median tempo 
median = df['Tempo'].median()
print(median)
#Seperate into groups if higher or lower than the median
df['Group'] = df['Tempo'].apply(lambda x: 'High' if x > median else 'Low')
#Find the average of each group
avg = df.groupby('Group')['Popularity'].mean()
#Sort in descending order
sorted = avg.sort_values(ascending=False)
#Make into a csv file
with open('tempo_popularity.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
#Format the headers and each column
    writer.writerow(['Tempo Category', 'Average Popularity'])
    for group, avg in sorted.items():
        writer.writerow([group, round(avg, 1)])


#4.Artists have the highest proportion of danceable songs
#Determine artists with highest percentage of danceable songs (>0.7)
df['High Danceability'] = df['Danceability'].apply(lambda x: 'high' if x > 0.7 else '')
#Count the total number of songs that an artist has
total = df.groupby('Artist').size().reset_index(name='Total Songs')
#Filter the songs that have a danceability score > 0.7
high_danceability = df[df['High Danceability'] == 'high']
#Group by the artists and count the number of songs that each artist wrote within the dataframe
high_danceability_counts = high_danceability.groupby('Artist').size().reset_index(name='Highly Danceable Songs')
#Check it all worked ok
#print(high_danceability_counts)
#Combine the two counts
merged = pd.merge(total, high_danceability_counts, on = 'Artist', how = 'left')
#Make NaN values so as not to affect the output of artists with 0 highly danceable songs
merged['Highly Danceable Songs'] = merged['Highly Danceable Songs'].fillna(0).astype(int)
#Find the percentage of each artists songs that are highly danceable
merged['Percent Danceable'] = (merged['Highly Danceable Songs'] / merged['Total Songs']).round(2)
#Sort by descending order
final_df = merged.sort_values(by='Percent Danceable', ascending=False)
#Make into a csv file
with open('danceable_artists.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
#Format the headers and each column
    writer.writerow(['Artist', 'Total Songs', 'Highly Danceable Songs', 'Percent Danceable'])
    for _, row in final_df.iterrows():
        writer.writerow([row['Artist'], row['Total Songs'], row['Highly Danceable Songs'], row['Percent Danceable']])
        

#5.Top 2 artists that released the most number of tracks in each tempo category
#Define the bins and labels
bins = [60, 70, 80, 100, 110, 156, 168, 200, float('inf')]
labels = ['Adagio', 'Andante', 'Moderato', 'Allegretto', 'Allegro', 'Vivace', 'Presto', 'Prestissimo']
#Format and add a new column to be organized by (so can draw data from later), categorize each track into each tempo group
df['Tempo Category'] = pd.cut(df['Tempo'], bins=bins, labels=labels, right=False)
#Group bu the the artist and tempo to count the number of tracks in each tempo group
tempo_groups = df.groupby(['Artist', 'Tempo Category']).size().reset_index(name='Track Count')
#Sort in descending order
tempo_groups_sorted = tempo_groups.sort_values(by=['Tempo Category', 'Track Count'], ascending=[True, False])
#Get the top 2 artist for each tempo group
top_artists = tempo_groups_sorted.groupby('Tempo Category').head(2).reset_index(drop=True)
#Make into a csv file
with open('tempo_binned.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
#Format the headers and each column
    writer.writerow(['Artist', 'Tempo Group', 'Number of Tracks'])
    for _, row in top_artists.iterrows():
        writer.writerow([row['Artist'], row['Tempo Category'], row['Track Count']])
