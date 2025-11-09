import pandas as pd
import glob
import os

# Path to your data folder (adjust if needed)
data_folder = 'data'

# Use glob to find all CSV files in the folder
csv_files = glob.glob(os.path.join(data_folder, '*.csv'))

# List to hold DataFrames
dfs = []

for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all DataFrames vertically (stack rows)
merged_df = pd.concat(dfs, ignore_index=True)

# Save merged DataFrame to a new CSV file
merged_df.to_csv('merged_output.csv', index=False)

print(f"Merged {len(csv_files)} CSV files into 'merged_output.csv'")
