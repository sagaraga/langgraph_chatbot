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