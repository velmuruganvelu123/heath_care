
import sqlite3
import pandas as pd

# Define file paths
DB_PATH = r"E:\Healthcare_chat_AI\data\veludb.db"
file_path = r"E:\Healthcare_chat_AI\data\healthcare_dataset.csv"

# Load CSV into a Pandas DataFrame
df = pd.read_csv(file_path)

# Print original column names to debug potential issues
print("Original CSV Columns:", df.columns.tolist())

# Define column name mapping
column_mapping = {
    "Blood Type": "Blood_Type",
    "Medical Condition": "Medical_Condition",
    "Date of Admission": "Date_of_Admission",
    "Insurance Provider": "Insurance_Provider",
    "Billing Amount": "Billing_Amount",
    "Room Number": "Room_Number",
    "Admission Type": "Admission_Type",
    "Discharge Date": "Discharge_Date",
}

# Rename columns only if they exist in the CSV
df.rename(columns=column_mapping, inplace=True)

# Print updated column names to confirm the change
print("Updated Columns:", df.columns.tolist())

# Ensure all necessary columns exist
for col in column_mapping.values():
    if col not in df.columns:
        print(f"Error: Column '{col}' is missing after renaming! Check CSV headers.")

# Clean the data
df["Age"] = pd.to_numeric(df["Age"], errors="coerce").fillna(0).astype("Int64")
df["Billing_Amount"] = pd.to_numeric(df["Billing_Amount"], errors="coerce").fillna(0.0)

# Convert date columns if they exist
for col in ["Date_of_Admission", "Discharge_Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

# Connect to SQLite database
conn = sqlite3.connect("veludb.db")
cursor = conn.cursor()

# Create table with correct column names
cursor.execute("""
CREATE TABLE IF NOT EXISTS healthcare_data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Age INTEGER,
    Gender TEXT,
    Blood_Type TEXT,
    Medical_Condition TEXT,
    Date_of_Admission TEXT,
    Doctor TEXT,
    Hospital TEXT,
    Insurance_Provider TEXT,
    Billing_Amount REAL,
    Admission_Type TEXT,
    Discharge_Date TEXT,
    Medication TEXT,
    Test_Results TEXT
)
""")

# Insert data into the database
df.to_sql("healthcare_data", conn, if_exists="replace", index=False)

# Commit and close connection
conn.commit()
conn.close()

print("Healthcare CSV cleaned and imported successfully!")
