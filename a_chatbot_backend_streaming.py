from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing import List, Annotated

from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict

class ChatBot(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

model = ChatOpenAI()

def chat_node(state: ChatBot):
    response = model.invoke(state['messages']).content
    return {'messages': [response]}

graph = StateGraph(ChatBot)

graph.add_node(chat_node, name="chat_node")
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

checkpointer = InMemorySaver()
chat_bot = graph.compile(checkpointer=checkpointer)

for chatbot_stream, metadata in chat_bot.stream(
    {'messages': [HumanMessage(content="Generate 500 words on indian cricket team")]},
    config={'configurable': {'thread_id': 'thread-1'}},
    stream_mode='messages'
):
    if chatbot_stream.content:
        print(chatbot_stream.content, end='', flush=True)
