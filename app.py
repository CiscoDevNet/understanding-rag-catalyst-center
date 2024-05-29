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
  model="llama3"
)

# DataHandler is not needed

# ======================
# Chainlit functions
# docs: https://docs.chainlit.io/get-started/overview
# ======================

@cl.on_chat_start
def on_chat_start():
  log.info("A new chat session has started!")

@cl.on_message
async def main(message: cl.Message):
  """
  This function is called every time a user inputs a message in the UI.
  It sends back an intermediate response from the tool, followed by the final answer.

  Args:
     message: The user's message.
  """

  # trick for loader: https://docs.chainlit.io/concepts/message
  msg = cl.Message(content="")
  await msg.send()

  msg.content = await ask_llm(message.content)

  await msg.update()

@cl.step
async def ask_llm(query_string):
  """
  Chainlit Step function: ask the LLM + return the result
  """
  response = LLM.ask_llm_rag(query_string)
  return response