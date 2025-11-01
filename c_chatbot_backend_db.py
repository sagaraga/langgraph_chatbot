from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import List, Annotated
import sqlite3

from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict

class ChatBot(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

model = ChatOpenAI()

def chat_node(state: ChatBot):
    # model.invoke(...) may return a message-like object; using .content gives a string.
    # Wrap the model's text response in an AIMessage so downstream code recognizes it as an assistant message.
    response_text = model.invoke(state['messages']).content
    return {'messages': [AIMessage(content=response_text)]}

graph = StateGraph(ChatBot)

graph.add_node(chat_node, name="chat_node")
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

conn = sqlite3.connect('chatbot_checkpoint.db', check_same_thread=False)

checkpointer = SqliteSaver(conn)
chat_bot = graph.compile(checkpointer=checkpointer)

# CONFIG = {'configurable': {'thread_id': 'thread-1'}}
# response = chat_bot.invoke(
#     {'messages': [HumanMessage(content="How to become a better developer with my name")]},
#     config=CONFIG
# )

# print(response)

def retrieve_all_threads():
    all_threads = set()
    threads = checkpointer.list(None)
    for thread in threads:
        all_threads.add(thread.config['configurable']['thread_id'])
    return list(all_threads)

