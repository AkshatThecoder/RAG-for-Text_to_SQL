# 🎯 RAG-powered Text-to-SQL Converter

## 🚀 Overview

This project implements a **Retrieval-Augmented Generation (RAG) pipeline** to convert **natural language questions into SQL queries**. It leverages **LangChain**, **OpenAI's LLM**, and **Streamlit** for an interactive user experience.

## ✨ Features

✅ **Natural Language to SQL**: Convert text-based queries into structured SQL.  
✅ **RAG-based Enhancement**: Ensures better query accuracy by retrieving schema context.  
✅ **Streamlit UI**: User-friendly interface for query generation.  
✅ **Supports Multiple Databases**: Works with PostgreSQL, MySQL, SQLite, etc.  
✅ **Deployable on Render**: Easily deployable with minimal setup.  

## 🛠️ Tech Stack

- **Python** 🐍  
- **LangChain** 🧠  
- **OpenAI GPT** 🤖  
- **FAISS Vector Store** 🔍  
- **SQLAlchemy** 🗄️  
- **Streamlit** 🎨  
- **Render (Deployment)** 🌐  

## 🔧 Installation & Setup

### 1️⃣ Clone the repository
```git clone https://github.com/yourusername/RAG-Text-to-SQL.git```

```cd RAG-Text-to-SQL```

### 2️⃣ Install dependencies
```pip install -r requirements.txt```

### 3️⃣ Set up environment variables
``` Create a .env file and add the following:```

```OPENAI_API_KEY=your_openai_key```

```DB_CONNECTION_STRING=your_database_url```


### 4️⃣ Run the application
``` streamlit run app.py ```

## 🚀 Deployment on Streamlit
``` 1.Push your project to GitHub. ```

``` 2.Log in on Streamlit.```

``` 3.Select your repo that you want to host.```

``` 4.Seltect a domain Click Deploy and access your live app!```

This project is licensed under the **MIT License**.