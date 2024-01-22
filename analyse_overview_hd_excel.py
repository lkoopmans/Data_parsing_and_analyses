import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# Path to your Excel file
excel_file_path = 'Overview_hds.xlsx'

# Read the Excel file
df = pd.read_excel(excel_file_path)

# Function to rearrange the elements
def rearrange_values(value):
    parts = value.split('_')
    # Rearrange the parts as needed, this example swaps the first and the last parts
    parts[0], parts[-1] = parts[-1], parts[0]
    return '_'.join(parts)

# Apply the function to the second column
df['Column1'] = df['Column1'].apply(rearrange_values)
# Sort
df = df.sort_values(by=df.columns[1])

df['Column4'] = np.floor(df['Column5']/3.9)

plt.figure()
plt.scatter(df['Column1'], df['Column4']*((8+51/60))/60)
# Rotate x-axis labels by 90 degrees
plt.xticks(rotation=90)

# Display only every 5th tick on the x-axis
plt.xticks(ticks=[tick for i, tick in enumerate(df['Column1']) if i % 5 == 0])
plt.ylabel('Deployment length [h]')
plt.xlabel('Date')
plt.show()

# Count the occurrences of each combination
combination_counts = df.groupby(['Column1', 'Column2']).size().reset_index(name='Counts')

# Display the result
print(combination_counts)

print('Total data: ', np.sum(df['Column5'])/1000, 'TB')
print('Total of: ', np.sum(df['Column4']), 'Chapters')
print('Total of: ', len(np.unique(df['HD NAME'])), 'HDs')