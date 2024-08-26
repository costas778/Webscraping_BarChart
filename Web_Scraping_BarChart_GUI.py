
#################################################################
#version 2 with bar chart as well
#################################################################

import numpy as np
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# URL of the page containing corruption data
URL = "https://worldpopulationreview.com/country-rankings/most-corrupt-countries"

# Fetch the webpage content
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the table content as a string
table_html = str(soup)

# Use StringIO to wrap the HTML string (addressing the FutureWarning)
table_io = StringIO(table_html)

# Parse the table using pandas (ensuring html5lib is installed)
try:
    tables = pd.read_html(table_io, flavor='html5lib')  # Specify 'html5lib' to avoid ImportError
except ImportError:
    raise ImportError("html5lib is required to parse the HTML. Please install it using 'pip install html5lib'.")

# Select the table of interest
df = tables[1]  # Adjust the index based on the specific table you need

# Save the DataFrame to a CSV file
df.to_csv('Corrupt_data2.csv', index=False)

# Load data into an SQLite database
conn = sqlite3.connect('Corrupt_data2.db')
df.to_sql('CorruptData', conn, index=False, if_exists='replace')

# Example query: Select specific rows or columns
query = "SELECT * FROM CorruptData WHERE Country IN ('Russia', 'Ukraine', 'Belarus', 'Cyprus')"
df_result = pd.read_sql_query(query, conn)

# Create a simple GUI to display the data and plot options
root = tk.Tk()
root.title("Corrupt Country Scores")

# Frame to hold the graph
graph_frame = tk.Frame(root)
graph_frame.pack(expand=True, fill=tk.BOTH)

# Dropdown to select the year
selected_year = tk.StringVar(value='Corruption Index 2022')
year_dropdown = ttk.Combobox(root, textvariable=selected_year, values=[
    'Corruption Index 2020', 'Corruption Index 2021', 'Corruption Index 2022'])
year_dropdown.pack()

# Add the data table to the GUI
tree = ttk.Treeview(root, columns=list(df_result.columns), show='headings')
for col in df_result.columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

for index, row in df_result.iterrows():
    tree.insert("", tk.END, values=list(row))

tree.pack(expand=True, fill=tk.BOTH)

# Function to update the bar graph based on the selected year
def update_graph():
    year_column = selected_year.get()
    if year_column in df_result.columns:
        # Clear the previous graph
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Create a new figure
        fig, ax = plt.subplots()

        # Bar graph settings
        ax.bar(df_result['Country'], df_result[year_column], color=['red', 'green', 'blue', 'orange'])

        ax.set_xlabel('Country')
        ax.set_ylabel(year_column)
        ax.set_title(f'Corruption Index by Country for {year_column.split()[-1]}')
        ax.set_ylim(0, df_result[year_column].max() + 5)  # Adjust y-axis limit

        # Embed the bar graph in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)
    else:
        print(f"Column '{year_column}' not found in the data.")

# Button to update the graph
update_button = ttk.Button(root, text="Update Graph", command=update_graph)
update_button.pack()

# Initial graph display
update_graph()

root.mainloop()

conn.close()
