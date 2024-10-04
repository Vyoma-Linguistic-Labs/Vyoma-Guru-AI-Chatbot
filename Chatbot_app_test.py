# Importing required packages
import streamlit as st
import time
from openai import OpenAI

# Set your OpenAI API key and assistant ID here
api_key = st.secrets["openai_apikey"]
assistant_id = st.secrets["assistant_id"]

# Set openAi client , assistant ai and assistant ai thread
@st.cache_resource
def load_openai_client_and_assistant():
    client = OpenAI(api_key=api_key)
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    return client, my_assistant, thread

client, my_assistant, assistant_thread = load_openai_client_and_assistant()

# check in loop if assistant ai parse our request
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# initiate assistant ai response
def get_assistant_response(user_input=""):
    message = client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=user_input,
    )
    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=assistant_id,
    )
    run = wait_on_run(run, assistant_thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=assistant_thread.id, order="asc", after=message.id
    )
    return messages.data[0].content[0].text.value

# Initialize session state variables if not already done
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # To store the entire chat history

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''
    # Append the user input to the chat history
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.user_input})
    # Get the assistant's response
    assistant_response = get_assistant_response(st.session_state.user_input)
    # Append the assistant's response to the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

# Set up the chatbot interface
st.markdown("<h1 style='text-align: center;'>संस्कृत सेवा सारथिः</h1>", unsafe_allow_html=True)

# Display the entire chat history with the latest messages at the bottom
chat_container = st.container()

# Display chat messages in normal order (latest at the bottom)
with chat_container:
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"<div style='text-align: right; background-color: #E1FFC7; padding: 5px; border-radius: 5px; margin: 5px; color: black;'>{entry['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color: #F1F0F0; padding: 5px; border-radius: 5px; margin: 5px; color: black;'>{entry['content']}</div>", unsafe_allow_html=True)

# Make sure the text input stays at the bottom
st.text_input("पृच्छतु", key='query', on_change=submit, placeholder="Send a message...")
