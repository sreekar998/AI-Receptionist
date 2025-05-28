"""
Simple in-memory memory for agent executors.
"""
from langchain.memory import ConversationBufferMemory

class SimpleMemory(ConversationBufferMemory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
