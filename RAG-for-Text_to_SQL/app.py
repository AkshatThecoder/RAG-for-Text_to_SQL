# Description: Streamlit app for Text-to-SQL using Perplexity API and SQLite database.

import streamlit as st
import sqlite3
import os
import re
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatPerplexity
from langchain.prompts import PromptTemplate
from db_schema_logic import extract_schema

# Set Perplexity API Key
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY:
    st.error("❌ Perplexity API Key not found! Set it as an environment variable.")
    st.stop()

# Streamlit UI
st.title("📊 Advanced RAG for Text-to-SQL")

# Drag & Drop DB Upload
uploaded_file = st.file_uploader("💾 Drag & Drop Your SQLite `.db` File Here", type="db")

if uploaded_file:
    # Save uploaded DB to a temporary file
    db_path = "uploaded_database.db"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Database uploaded successfully!")

    # Extract Schema from the uploaded DB
    db_schema = extract_schema(db_path)
    st.text_area("📜 Extracted Database Schema", db_schema, height=200)

    # User Input for Text Query
    question = st.text_input("🔍 Ask a question in natural language:")

    if st.button("Generate SQL Query"):
        if question:
            # Load LLM for Text-to-SQL
            llm = ChatPerplexity(model="pplx-7b-online", api_key=PERPLEXITY_API_KEY)
            prompt = PromptTemplate(
                input_variables=["schema", "question"],
                template="Given the database schema:\n{schema}\n\nConvert this natural language question into an SQL query:\n{question}",
            )
            from langchain.schema.runnable import RunnableLambda
            chain = prompt | llm | RunnableLambda(lambda x: x.content if hasattr(x, "content") else str(x))

            # Generate SQL Query
            response = chain.invoke({"schema": db_schema, "question": question})
            
            # ✅ Extract SQL query using regex (Ensures only one statement)
            match = re.search(r"(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|WITH|PRAGMA)[^;]*;", response, re.IGNORECASE)

            if match:
                sql_query = match.group(0).strip()
            else:
                sql_query = None

            if sql_query:
                # ✅ Fix: Ensure only one valid SQL statement
                sql_query = sql_query.split(";")[0] + ";"  # Keeps only the first statement

                st.code(sql_query, language="sql")

                # Execute the Query on the Uploaded Database
                conn = sqlite3.connect(db_path)
                try:
                    cursor = conn.cursor()
                    cursor.execute(sql_query)  # ✅ Only runs a single statement
                    result = cursor.fetchall()
                    conn.commit()
                    conn.close()

                    if result:
                        st.write("### Query Results:")
                        st.dataframe(result)
                    else:
                        st.info("✅ Query executed successfully, but no results were returned.")
                
                except sqlite3.Error as e:
                    st.error(f"❌ Error executing query: {e}")
                    conn.close()
            else:
                st.error("❌ Could not extract a valid SQL query from the LLM response. Try rephrasing your question.")

