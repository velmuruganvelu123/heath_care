import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Missing API Key! Please set GROQ_API_KEY in the .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Page configuration
st.set_page_config(page_title="Healthcare Data Chatbot", page_icon="🏥")

st.title("🏥 Healthcare Data Insights Chatbot")
st.write("Ask anything related to the Healthcare Database!")

# Custom CSS for chat styling
st.markdown("""
    <style>
        .chat-bubble {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .user-bubble {
            background-color: #DCF8C6;
            text-align: right;
        }
        .assistant-bubble {
            background-color: #ECECEC;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
    You are an AI SQL assistant specialized in Supabase relational databases.
    Your task is to generate optimized, safe, and accurate SQL queries based on user requests.

    **Rules:**
    - Always generate a **valid SQL query** for Supabase in **PostgreSQL syntax**.
    - Use **double quotes (`"column_name"`)** to reference column names.
    - Use **table-qualified column names** in the format `health_care."Column_Name"`.
    - Ensure the **output is ONLY the SQL query** with **no extra words, explanations, or formatting**.
    - Always include `LIMIT 10` in queries.

    **Example Inputs & Outputs:**
    - **User:** `"How many patients are above 30 years old?"`  
    - **Assistant Output:**  
    ```
    SELECT COUNT(health_care."Name")  
    FROM health_care  
    WHERE "Age" > 30  
    LIMIT 10;
    ```

    - **User:** `"Find all female patients in the hospital."`  
    - **Assistant Output:**  
    ```
    SELECT *  
    FROM health_care  
    WHERE "Gender" = 'Female'  
    LIMIT 10;
    ```
    """}
]


# User input
user_input = st.text_input("You:", "")
if user_input:
    st.session_state.messages.append({"role": "user", "content": f"This is user Query : {user_input}. you have to return only SQL Query , don't return any other words  from the response."})
    
    try:
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display chat history
st.write("## Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-bubble user-bubble'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div class='chat-bubble assistant-bubble'><strong>Assistant:</strong> {message['content']}</div>", unsafe_allow_html=True)