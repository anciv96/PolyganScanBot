import pandas as pd
from sqlalchemy import create_engine

# Step 1: Load the Excel File
excel_file_path = '../../../our_addresses/Far holders (1).xlsx'
sheet_name = 'Token Unlock wallets'  # Change this to the name of your sheet if needed

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name=sheet_name, engine='openpyxl')

# Step 2: Connect to SQLite Database
db_path = 'sqlite:///../../../db.db'
engine = create_engine(db_path)

# Step 3: Write DataFrame to SQLite Table
table_name = 'our_token'  # Name of the table where data should be stored

# Writing the DataFrame to SQLite
df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data from {sheet_name} has been successfully written to the {table_name} table in the SQLite database.")
