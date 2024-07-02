from pandasai import SmartDataframe
from pandasai.llm import GooglePalm
import streamlit as st
import pandas as pd
import sqlite3
import os

def chat_with_csv(df, query):
    llm = GooglePalm(api_key="AIzaSyCFZdU4u6NSI1iqHdDeHK2YOLOq6k3fN2M")
    pandas_ai = SmartDataframe(df, config={"llm": llm})
    return pandas_ai.chat(query)

def chat_with_db(conn, query):
    pandas_ai = SmartDataframe(conn, config={"llm": GooglePalm(api_key="AIzaSyCFZdU4u6NSI1iqHdDeHK2YOLOq6k3fN2M")})
    return pandas_ai.chat(query)

st.set_page_config(layout='wide')
st.title("Chat with Data")

# Select data source
data_source = st.sidebar.selectbox("Choose your data source:", ["CSV", "Database"])

if data_source == "CSV":
    input_csvs = st.sidebar.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=False)
    if input_csvs:
        data = pd.read_csv(input_csvs)
        st.info("CSV uploaded successfully.")
elif data_source == "Database":
    db_file = st.sidebar.file_uploader("Upload your SQLite Database file", type=['db'], accept_multiple_files=False)
    if db_file:
        conn =  SqliteConnector(config={"database" : "db_file"})
        st.info("Database connected successfully.")

input_text = st.text_area("Enter the query:")
if st.button("Submit"):
    if input_text:
        if data_source == "CSV" and input_csvs:
            result = chat_with_csv(data, input_text)
        elif data_source == "Database" and db_file:
            result = chat_with_db(conn, input_text)

        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        elif isinstance(result, str) and result.endswith(".png"):
            image_path = os.path.join('/mount/src/chat-with-multiple-csv/exports/charts', result)
            st.image(image_path)
        else:
            st.success(result)
    else:
        st.error("Please enter a query.")

# Ensure to close the database connection properly if it's open
if 'conn' in locals():
    conn.close()
