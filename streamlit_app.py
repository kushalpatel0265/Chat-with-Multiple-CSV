from pandasai import SmartDataframe
from pandasai.llm import GooglePalm
import streamlit as st
import pandas as pd
import os

def chat_with_csv(df, query):
    llm = GooglePalm(api_key="AIzaSyCFZdU4u6NSI1iqHdDeHK2YOLOq6k3fN2M")
    pandas_ai = SmartDataframe(df, config={"llm": llm})

    result = pandas_ai.chat(query)
    return result

def submit_query():
    input_text = st.session_state.input_text
    if input_text:
        result = chat_with_csv(data, input_text)
        if isinstance(result, pd.DataFrame):
            # Convert DataFrame to markdown for display purposes
            result = "Data Table Displayed Below"
            st.session_state.chat_history.append((input_text, result))
            st.session_state.displayed_result = result
        elif isinstance(result, str) and result.endswith(".png"):
            image_path = os.path.join('/mount/src/chat-with-multiple-csv/exports/charts', result)
            st.session_state.chat_history.append((input_text, "Image Displayed Below"))
            st.session_state.displayed_result = image_path
        else:
            st.session_state.chat_history.append((input_text, result))
            st.session_state.displayed_result = result
        # Clear the text area after submission
        st.session_state.input_text = ""
    else:
        st.error("Please enter a query to chat with the CSV data.")

st.set_page_config(layout='wide')
st.title("Chat with Multiple CSV")

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'displayed_result' not in st.session_state:
    st.session_state.displayed_result = None

input_csvs = st.sidebar.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)

if input_csvs:
    selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)

    st.info("CSV uploaded successfully")
    data = pd.read_csv(input_csvs[selected_index])

    # Layout for chat-like interface
    col1, col2 = st.columns([1, 4])  # Adjust the size ratio based on your preference

    with col1:
        st.write("### History")
        for idx, (question, answer) in enumerate(st.session_state.chat_history, start=1):
            st.write(f"Q{idx}: {question}")
            st.write(f"A{idx}: {answer}")
            st.markdown("---")

    with col2:
        st.text_area("Enter your query", key='input_text', on_change=None)
        if st.button("Submit", on_click=submit_query):
            pass  # Button action is handled by the submit_query function

        # Display the result dynamically based on what was set in submit_query
        if st.session_state.displayed_result:
            if isinstance(st.session_state.displayed_result, str) and st.session_state.displayed_result.endswith(".png"):
                st.image(st.session_state.displayed_result)
            else:
                st.write(st.session_state.displayed_result)
