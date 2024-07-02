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

# Initialize or extend the chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

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
        input_text = st.text_area("Enter your query", "")

        if st.button("Submit", key="submit"):
            if input_text:
                result = chat_with_csv(data, input_text)
                if isinstance(result, pd.DataFrame):
                    # Convert DataFrame to markdown for display purposes
                    result = "Data Table Displayed Below"
                    st.session_state.chat_history.append((input_text, result))
                    st.dataframe(result)
                elif isinstance(result, str) and result.endswith(".png"):
                    image_path = os.path.join('/mount/src/chat-with-multiple-csv/exports/charts', result)
                    st.session_state.chat_history.append((input_text, "Image Displayed Below"))
                    st.image(image_path)
                else:
                    st.session_state.chat_history.append((input_text, result))
                    st.success(result)
            else:
                st.error("Please enter a query to chat with the CSV data.")
            # Clear the text area after submission
            st.session_state.input_text = ""
