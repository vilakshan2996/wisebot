import streamlit as st
import langchain_helper as lh
import random
import time
import memory as mem
import numpy as np
import json
import streamlit as st
import streamlit_lottie
from streamlit_lottie import st_lottie


        
# Define a function to load Lottie files
@st.cache_data
def load_lottiefile(file_path):
    print("HI")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            with st.sidebar.container():
                st_lottie(json.load(f), speed=1, reverse=False, loop=True, quality="low", height=200)
    except Exception as e:
        st.error(f"Error loading the JSON file: {e}")   


# Define a custom theme using Streamlit's theme configuration
st.set_page_config(
    page_title="GTN Wisess Bot",
    page_icon=":robot_face:",
    layout="wide",  # You can adjust this as needed
    initial_sidebar_state="auto",
      # Set the background color
)
st.title("GTN WiseBot")
# "st.session_state_object:",st.session_state
memory = mem.load_memory(st)
load_lottiefile("robo.json")


# Place the Lottie animation inside the sidebar


   
def model_callback():
    st.session_state["collection"] = st.session_state["collection_selected"]
    lh.loadData(st.session_state["collection"])
    del st.session_state["messages"]
    

if "collection" not in st.session_state:
    st.session_state["collection"] = "support"
    lh.loadData(st.session_state["collection"])

st.session_state.collection = st.sidebar.selectbox(
    "Select Chat Bot",
    ("support", "devops"),
    index=0 if st.session_state["collection"] == "support" else 1,
    on_change=model_callback,
    key="collection_selected",
) 




if prompt := st.chat_input():
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = lh.execute_qa(prompt,memory.load_memory_variables({})["history"])
    
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
