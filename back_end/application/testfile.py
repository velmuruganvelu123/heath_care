import os
import sqlite3
from groq import Groq

# Load Groq API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Define the database schema
schema_definition = """
Table: healthcare_data
Columns:
- ID (INTEGER PRIMARY KEY): Unique patient ID
- Name (TEXT): Patient's name
- Age (INTEGER): Patient's age
- Gender (TEXT): Gender of the patient
- Blood_Type (TEXT): Blood type of the patient
- Medical_Condition (TEXT): Diagnosed medical condition
- Date_of_Admission (TEXT): Date of hospital admission
- Doctor (TEXT): Attending doctor
- Hospital (TEXT): Hospital name
- Insurance_Provider (TEXT): Insurance company
- Billing_Amount (REAL): Total medical bill
- Admission_Type (TEXT): Type of admission (Emergency/Elective)
- Discharge_Date (TEXT): Date of discharge
- Medication (TEXT): Prescribed medication
- Test_Results (TEXT): Lab test results
"""

# Function to generate SQL query from natural language
def get_sql_query(natural_language_query):
    """
    Converts a natural language query into an SQL query using an LLM.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that converts natural language queries into SQL queries for a healthcare database. "
                "The database schema is as follows:\n"
                f"{schema_definition}\n"
                "Ensure the SQL query is syntactically correct and optimized. "
                "Return **only** the SQL query without explanations, comments, or additional text."
            ),
        },
        {
            "role": "user",
            "content": f"Convert this natural language query to an SQL query: '{natural_language_query}'",
        },
    ]

    try:
        completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating SQL query: {str(e)}"

# Function to execute the SQL query
def execute_sql_query(sql_query):
    """
    Executes an SQL query and returns the results.
    """
    database = "veludb.db"  # Ensure this is the correct database

    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Extract column names
        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        conn.close()

        if not rows:
            return {"status": "success", "data": "No matching records found."}

        # If the query is a COUNT query, extract the number directly
        if "COUNT" in sql_query.upper():
            return {"status": "success", "data": f"There are {rows[0][0]} matching records."}

        # Format the data output
        formatted_data = [dict(zip(columns, row)) for row in rows]
        return {"status": "success", "data": formatted_data}

    except Exception as e:
        return {"status": "error", "message": f"Query execution failed: {str(e)}"}

# Function to refine the response using another LLM
def refine_response(user_query, sql_data):
    """
    Uses another LLM to generate a natural language response from the SQL query and its result.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that summarizes SQL query results into clear, user-friendly responses. "
                "Given a user query, an SQL query, and the extracted data, provide a concise and informative response."
            ),
        },
        {
            "role": "user",
            "content": f"User Query: {user_query}\nSQL Data: {sql_data}\n"
                       f"Please summarize this data in a natural and informative way. don't say like this Based on the provided SQL query and data, I can summarize the result as follows:According to the query,",
        },
    ]

    try:
        completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error refining response: {str(e)}"

# Example Usage
if __name__ == "__main__":
    # Example user query
    user_query = "How many male patients are there?"

    # Step 1: Convert natural language query to SQL
    sql_query = get_sql_query(user_query)
    print("Generated SQL Query:\n", sql_query)

    # Step 2: Execute SQL query and fetch results
    query_result = execute_sql_query(sql_query)
    print("Query Result:\n", query_result)

    # Step 3: Refine the response using another LLM
    refined_response = refine_response(user_query, sql_query, query_result["data"])
    print("Refined Response:\n", refined_response)
