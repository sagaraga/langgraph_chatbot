import streamlit as st
from a_chatbot_backend import chat_bot
from langchain_core.messages import HumanMessage, AIMessage
import uuid

########### utility functions ###########

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state["messages"] = []
    st.session_state["thread_id"] = generate_thread_id()
    add_chat_thread(st.session_state["thread_id"])

def add_chat_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    # Placeholder for loading conversation logic
    state = chat_bot.get_state({'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

###########################################

############### session state management ###############

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_chat_thread(st.session_state["thread_id"])

###################################################

st.session_state["messages"] = st.session_state.get("messages", [])

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


st.sidebar.title("Sagar's Customized Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Chat History")

for thread_id in st.session_state["chat_threads"]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)

        tmp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                tmp_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                tmp_messages.append({"role": "assistant", "content": msg.content})

        st.session_state["messages"] = tmp_messages


CONFIG = {'configurable':{'thread_id':st.session_state["thread_id"]}}


st.title("Welcome to the Streamlit Frontend!")

for message  in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input('Type your message here...')


if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)


    # st.session_state["messages"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            chatbot_stream.content for chatbot_stream, metadata in chat_bot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )
        st.session_state["messages"].append({"role": "assistant", "content": ai_message})