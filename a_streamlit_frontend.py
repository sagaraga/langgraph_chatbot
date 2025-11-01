import streamlit as st
from a_chatbot_backend import chat_bot
from langchain_core.messages import HumanMessage, AIMessage

CONFIG = {'configurable':{'thread_id':'thread-1'}}

st.title("Welcome to the Streamlit Frontend!")

st.session_state["messages"] = st.session_state.get("messages", [])

for message  in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input('Type your message here...')


if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    response = chat_bot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

    ai_message = response['messages'][-1].content

    st.session_state["messages"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)