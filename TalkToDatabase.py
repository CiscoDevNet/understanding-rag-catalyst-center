"""
Cisco Sample Code License 1.1
Author: flopach 2025
"""
import chromadb
import os
import logging
log = logging.getLogger("applogger")

class VectorDB:
  def __init__(self, collection_name, database_path):
    """
    Create new VectorDB instance

    Args:
        collection_name (str): Name of the collectiong
        database_path (str): persistent storage for vectorDB
    """

    # set chromadb client
    self.chromadb_client = chromadb.PersistentClient(path=database_path)

    # set embeddings function
    self.embeddings_function = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
    
    # set (or create) collection
    self.collection = self.chromadb_client.get_or_create_collection(
      name=collection_name,
      embedding_function=self.embeddings_function
    )

  def query_db(self, query_string, n_results):
    """
    Query the vector DB

    Args:
        query_string (str): specific query string
        n_results (int): Number of documents return by vectorDB query
    """

    # define vectorDB search
    # docs: https://docs.trychroma.com/reference/Collection#query

    results = self.collection.query(
      query_texts=[query_string],
      n_results=n_results
    )

    # Display queried documents
    log.debug(f'Queried documents: {results["metadatas"]}')
    log.debug(f'Queried distances: {results["distances"]}')

    return results["documents"]
  
  def collection_add(self,documents,ids,metadatas=None):
    """
    Add to collection

    Args:
        documents (dict): list of chunked documents
        ids (dict): list of IDs
        metadatas (dict): list of metadata
    """
    r = self.collection.add(
      documents=documents,
      ids=ids,
      metadatas=metadatas,
    )
    if r != None:
      log.warning(f"{ids} returned NOT None...")