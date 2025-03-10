import os
from langchain.schema import AIMessage
import sys
import streamlit as st
import unicodedata
from dotenv import load_dotenv
from db_schema_logic import setup_llm_chain
from db_connector import get_schema, execute_query

# Force UTF-8 Encoding to prevent Unicode errors
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

# Load API Key from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Ensure API key is correctly formatted
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing! Please set it in the .env file.")
groq_api_key = groq_api_key.strip().replace("“", "").replace("”", "")

# Function to Normalize Text
def normalize_text(text):
    """Convert special Unicode characters to standard ASCII format."""
    if text:
        return unicodedata.normalize("NFKD", text).encode("utf-8", "ignore").decode("utf-8")
    return text

# Set up Streamlit Page
st.set_page_config(page_title="Advanced RAG: Text-to-SQL")
st.title("🔍 Advanced RAG: Database Text-to-SQL Chatbot")

# Load & Normalize Database Schema
db_schema = get_schema()
db_schema = normalize_text(db_schema)

# Display Schema for Debugging
# st.write("### Database Schema Loaded:")
# st.code(db_schema, language="sql")

# User Input
question = st.text_area("Ask a question about the database:")
question = normalize_text(question)

if st.button("Generate SQL Query"):
    if not groq_api_key:
        st.error("⚠️ GROQ_API_KEY is missing! Please set it in the .env file.")
    elif not question.strip():
        st.error("⚠️ Please enter a question.")
    else:
        with st.spinner("Generating SQL Query..."):
            chain = setup_llm_chain()
            response = chain.invoke({"schema": db_schema, "question": question})

            # Ensure AI response is a string
            if isinstance(response, AIMessage):
                response = response.content  # Extract AI-generated SQL query
            elif isinstance(response, dict) and "text" in response:
                response = response["text"]  # Handle dict responses
            response = str(response).strip()

            # Ensure response is a valid SQL query before execution
            if not response.lower().startswith("select"):
                st.warning("AI did not generate a valid SQL query.")
                st.error(f"Response received: {response}")
            else:
                st.success("SQL Query Generated:")
                st.code(response, language="sql")

                # Execute SQL Query
                with st.spinner("Executing Query..."):
                    result = execute_query(response)

                    if isinstance(result, str):  # If execution returns an error message
                        st.error(f"Error executing query: {result}")
                    elif result is None or result.empty:
                        st.warning("No data found for the query.")
                    else:
                        st.write("**Query Results:**")
                        st.dataframe(result)