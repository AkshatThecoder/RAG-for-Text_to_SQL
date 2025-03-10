from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import unicodedata
from langchain.schema.runnable import RunnableLambda
from langchain.schema import AIMessage

# Function to Normalize Text
def normalize_text(text):
    """Convert special Unicode characters to standard ASCII format."""
    if text:
        return unicodedata.normalize("NFKD", text).encode("utf-8", "ignore").decode("utf-8")
    return text

def extract_text(ai_message):
    """Ensure AI response is returned as a string."""
    if isinstance(ai_message, AIMessage):
        return ai_message.content  # Extract the actual text response
    elif isinstance(ai_message, dict) and "text" in ai_message:
        return ai_message["text"]  # Handle dict responses
    return str(ai_message)  # Convert unknown types to string

import sqlite3

def extract_schema(db_path):
    """Extracts the database schema from an SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        schema.append(f"Table: {table_name}")
        for col in columns:
            schema.append(f"- {col[1]} ({col[2]})")
        schema.append("")  # Add spacing

    conn.close()
    return "\n".join(schema)

def setup_llm_chain():
    """Set up LLM Chain for Text-to-SQL conversion using Groq."""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please check .env file.")

    llm = ChatGroq(
        model_name="llama3-8b-8192",
        api_key=api_key
    )

    prompt_template = normalize_text("""
    You are an AI assistant that generates SQL queries based on user requests.
    You have access to the following database schema:

    {schema}

    Based ONLY on this schema, generate a **valid SQL query** to answer the following question:

    {question}

    IMPORTANT:
    - Do NOT assume any missing data.
    - If the question refers to an event, search for an event with a similar name.
    - If no relevant data exists, return: "SELECT 'No matching data found' AS result;"
    - NEVER return an explanation, only return a SQL query.

    SQL Query:
    """)

    prompt = PromptTemplate(input_variables=["schema", "question"], template=prompt_template)

    return prompt | llm | RunnableLambda(extract_text)
