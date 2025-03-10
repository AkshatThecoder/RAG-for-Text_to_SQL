import sqlite3
import pandas as pd

DB_PATH = "new.db"

def get_schema():
    """Retrieve database schema as a string for LLM."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = ""
    for table in tables:
        table_name = table[0]
        schema += f"Table: {table_name}\n"

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        for col in columns:
            schema += f"- {col[1]} ({col[2]})\n"

        schema += "\n"

    conn.close()
    
    print("Database Schema Retrieved:")
    # print(schema)  # Debugging output

    return schema

def execute_query(query):
    """Execute a SQL query and return the results as a DataFrame."""
    try:
        conn = sqlite3.connect(DB_PATH)
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        return f"Error executing query: {str(e)}"
