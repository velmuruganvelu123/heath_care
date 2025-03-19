import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/get-response"

# Streamlit UI setup
st.set_page_config(page_title="Healthcare Chatbot", page_icon="🤖", layout="wide")
st.title("Healthcare Chatbot 🤖")
st.write("Hello! I'm your AI healthcare assistant. Ask me anything related to healthcare!")

# Sidebar for SQL Query
st.sidebar.header("🗄️ SQL Query")

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to FastAPI
    payload = {"prompt": user_input}
    try:
        response = requests.post(FASTAPI_URL, json=payload, timeout=10)
        if response.status_code == 200:
            response_data = response.json()

            # Extract SQL Query
            sql_query = response_data.get("query", "No SQL query generated.")

            # Fix: Handle both string and dictionary responses
            response_value = response_data.get("response", "No data available.")
            if isinstance(response_value, dict):
                result = response_value.get("data", "No data available.")
            else:
                result = response_value  # Use string directly

        else:
            sql_query = "N/A"
            result = "Error: Unable to retrieve data."

    except requests.exceptions.RequestException as e:
        sql_query = "N/A"
        result = f"Connection error: {str(e)}"
    except ValueError:
        sql_query = "N/A"
        result = "Error: Invalid JSON received."

    # Display SQL Query in Sidebar
    with st.sidebar:
        st.code(sql_query, language="sql")

    # Display Chatbot Response
    with st.chat_message("assistant"):
        st.markdown(f"### 📊 Result\n{result}")

    # Save response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"**Result:**\n{result}"
    })
