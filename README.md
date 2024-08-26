# Webscraping_BarChart

Key

**#Scrapes from this URL**
URL = "https://worldpopulationreview.com/country-rankings/most-corrupt-countries"

# Select the table of interest (There are two tables i.e. 0 and 1)
df = tables[1]  # Adjust the index based on the specific table you need

**#You can adjust the query to add and remove countries from the folllowing.**
query = "SELECT * FROM CorruptData WHERE Country IN ('Russia', 'Ukraine', 'Belarus', 'Cyprus')"

# Save the DataFrame to a CSV file
df.to_csv('Corrupt_data2.csv', index=False)

# Load data into an SQLite database
conn = sqlite3.connect('Corrupt_data2.db')
df.to_sql('CorruptData', conn, index=False, if_exists='replace')
