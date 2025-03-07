import os
import streamlit as st
from langchain_openai import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Configuration
st.set_page_config(page_title="Healthcare Data Chatbot", page_icon="🩺")
st.sidebar.title("Navigation")

# Retrieve API Keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Database Connection Setup
db_chain = None  # Initialize as None to prevent crashes
if SUPABASE_URL and SUPABASE_KEY:
    try:
        DATABASE_URL = f"postgresql://postgres:{SUPABASE_KEY}@{SUPABASE_URL.split('//')[1]}/postgres"
        # print(DATABASE_URL)
        engine = create_engine(
            DATABASE_URL,
            connect_args={"connect_timeout": 30},  # Increase timeout to 30 seconds
            pool_pre_ping=True,  # Keeps the connection alive
            pool_recycle=1800  # Refresh connection every 30 minutes
        )

        db = SQLDatabase(engine)
        # print(db)
        llm = OpenAI(api_key=GROQ_API_KEY, model_name="llama3-8b", temperature=0)
        db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db)
        st.success("✅ Connected to the database!")
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
else:
    st.error("⚠️ Database connection details are missing! Check your environment variables.")

# Streamlit UI
st.title("🩺 Healthcare Data Insights Chatbot")
st.write("Ask anything related to the Healthcare Database!")

# Query Input
query = st.text_area("Enter your question:")
if st.button("Submit"):
    if query:
        if db_chain:
            try:
                sql_query = db_chain.run(query)  # Convert LLM response to SQL
                st.write(f"🔍 **Generated SQL Query:** ```{sql_query}```")

                # Execute SQL Query
                with engine.connect() as connection:
                    result = connection.execute(text(sql_query))
                    # print(result)
                    data = result.fetchall()
                    data = [dict(row._mapping) for row in data]  # Convert rows to dictionary format

                # Display Results
                if data:
                    st.write("### 📊 Query Results:")
                    st.write(data)
                else:
                    st.warning("⚠️ No data found!")

            except Exception as e:
                st.error(f"⚠️ Query processing error: {e}")
        else:
            st.error("⚠️ Database chain is not initialized! Please check the connection.")
    else:
        st.warning("⚠️ Please enter a question!")

