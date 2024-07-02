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

st.set_page_config(layout='wide')
st.title("Chat with Multiple CSV")

input_csvs = st.sidebar.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)

if input_csvs:
    selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)

    st.info("CSV uploaded successfully")
    data = pd.read_csv(input_csvs[selected_index])

    # Store input text to keep it in the text area after submission
    input_text = st.text_area("Enter the query", value=st.session_state.get('input_text', ''))
    if st.button("Submit"):
        # Update session state to keep text after re-running the script
        st.session_state['input_text'] = input_text
        if input_text:
            result = chat_with_csv(data, input_text)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
            elif isinstance(result, str) and result.endswith(".png"):
                image_path = os.path.join('/mount/src/chat-with-multiple-csv/exports/charts', result)
                st.image(image_path)
            else:
                st.success(result)
        else:
            st.error("Please enter a query to chat with the CSV data.")
