"""
Cisco Sample Code License 1.1
Author: flopach 2024
"""
from TalkToOllama import LLMOllama
from TalkToDatabase import VectorDB
from ImportData import DataHandler
import logging
import chainlit as cl
log = logging.getLogger("applogger")
logging.getLogger("applogger").setLevel(logging.DEBUG)

# ======================
# Connection & Instances - Paste/edit here your code from the Jupyter Notebook
# ======================
vectordb = VectorDB(
  collection_name="catcenter_vectors",
  database_path="chromadb/"
)

LLM = LLMOllama(
  database=vectordb,
  model="llama3.1"
)

# DataHandler is not needed

# ======================
# Chainlit functions
# docs: https://docs.chainlit.io/get-started/overview
# ======================

@cl.on_chat_start
def on_chat_start():
  """
  Hook to react to the user websocket connection event.
  """
  log.info("A new chat session has started!")

@cl.on_message
async def main(message: cl.Message):
    """
    Chainlit Main function
    This function is called every time a user inputs a message in the UI
    """
    answer = await cl.make_async(sync_func)(message.content)
    await cl.Message(
        content=answer,
    ).send()

def sync_func(query_string):
    """
    Synchronous function for querying the LLM

    For long running synchronous tasks without blocking the event loop
    https://docs.chainlit.io/api-reference/make-async
    """
    return LLM.ask_llm_rag(query_string)