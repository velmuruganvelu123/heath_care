import os
import sqlite3
import pandas as pd

DB_PATH = r"E:/Healthcare_chat_AI/data/veludb.db"
# print("Database exists:", os.path.exists(DB_PATH))


def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM healthcare_data;"  # Fetch 5 rows
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df =fetch_data()
df.drop_duplicates(inplace=True)
# print(df)  # Display the first 5 rows



