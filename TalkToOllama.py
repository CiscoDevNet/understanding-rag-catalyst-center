"""
Cisco Sample Code License 1.1
Author: flopach 2025
"""
import ollama
import time
import logging
log = logging.getLogger("applogger")

class LLMOllama:
  def __init__(self, database, model = "llama3.1"):
    self.database = database
    self.model = model

  def ask_llm(self,query_string):
    """
    Ask the LLM with the query string.

    Args:
        query_string (str): user question
    """
    # response function
    response = ollama.chat(
      model=self.model,
      messages=[
        {
            "role": "system",
            "content": "You are a general helpful assistant to answer questions."
        },{
            'role': 'user',
            'content': query_string,
        }
      ]
    )
    return response


  def ask_llm_rag(self,query_string,n_results=5):
    """
    Ask the LLM with the query string.
    Search for context in vectorDB

    Args:
        query_string (str): details of the REST API call
        n_results (int): Number of documents return by vectorDB query
    """
    # Record the start time
    start_time = time.time()

    # context queries to vectorDB
    context = self.database.query_db(query_string,n_results)
    
    user_prompt = f'''User question: '{query_string}'
    Context delimited with XML tags: <context>{context}</context>
    Based on the context find the right REST API calls for the user question.
    Always list all available query parameters. Include the REST operation and query path.
    List all required steps and documentation.
    Create the source code for the user question in the programming language Python.
    Use the 'requests' Python library.
    If loops or advanced code is needed, provide it.
    Always include authentication and authorization in the Python code. The authentication process is explained delimited with XML tags: <auth>Every API query needs to include the header parameter 'X-Auth-Token' for authentication. This is where the access token is defined.If the user does not have the access token, the user needs to call the REST API query '/dna/system/api/v1/auth/token' to receive the access token. Only the API query '/dna/system/api/v1/auth/token' is using the Basic authentication scheme, as defined in RFC 7617. All other API queries need to have the header parameter 'X-Auth-Token' defined.</auth>
    Tell the user if you do not know the answer. 
    '''

    log.info(f"=== USER PROMPT === \n {user_prompt}")

    response = ollama.chat(model=self.model, messages=[
    {
        "role": "system",
        "content": """You are the Cisco Catalyst Center REST API and Python code assistant.
        You provide documentation and Python programming code for developers based on the user questions."""
    },{
        'role': 'user',
        'content': user_prompt,
    }
    ])

    # Calculate the total duration
    duration = round(time.time() - start_time, 2)
    exec_duration = f"The query '{query_string}' took **{duration} seconds** to execute."
    log.info(exec_duration)

    return response['message']['content']+"\n\n"+exec_duration