import pandas as pd

# Excel file paths
excel_file_path02 = "./processed_data_20240105112236.xlsx"
excel_file_path = "./processed_data_20240105174502.xlsx"

# Read Excel files into DataFrames
df1 = pd.read_excel(excel_file_path02)
df2 = pd.read_excel(excel_file_path)

# Find differences between the two DataFrames
differences = pd.concat([df1, df2]).drop_duplicates(keep=False).reset_index(drop=True)

# Print the differences
print("Differences between the two Excel files:")
print(differences)
