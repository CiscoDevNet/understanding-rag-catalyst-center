"""
Cisco Sample Code License 1.1
Author: flopach 2025
"""
import json
import glob
from bs4 import BeautifulSoup
import requests
import logging
log = logging.getLogger("applogger")

class DataHandler:
    def __init__(self, database):
        self.database = database

    def scrape_apidocs_catcenter(self):
        """
        Scrape developer.cisco.com Catalyst Center API docs, chunk it, and embed it into the vector database

        Return:
            None        
        """
        base_url = "https://developer.cisco.com/docs/dna-center/"

        docs_list = [
            "overview",
            "getting-started",
            "api-quick-start",
            "asynchronous-apis",
            "authentication-and-authorization",
            "command-runner",
            "credentials",
            "device-onboarding",
            "device-provisioning",
            "devices",
            "discovery",
            "events",
            "global-ip-pool",
            "health-monitoring",
            "path-trace",
            "rma-device-replacement",
            "reports",
            "software-defined-access-sda",
            "sites",
            "swim",
            "topology"
        ]
        
        for doc in docs_list:
            try:
                r = requests.get(base_url+doc)
                soup = BeautifulSoup(r.content, 'html.parser')
                chunks = self._chunk_text(soup.get_text(),512)

                log.info(chunks)

                self.database.collection_add(
                    documents=chunks,
                    ids=[f"{doc}_{x}" for x in range(len(chunks))],
                    metadatas=[{ "doc_type" : "apidocs" } for x in range(len(chunks))]
                )

                log.info(f"Scraped data from {base_url+doc}")

            except Exception as e:
                log.error(f"Error when requesting data from {base_url+doc}! Error: {e}")
        
        log.info(f"=== Done with api docs scraping ===")

    def import_apispecs_from_json(self):
        """
        This function is used to embed the already existing EXTENDED API specification.
        The data was generated with GPT-3.5-turbo.

        Return:
            None
        """
        # open openAPI specs file
        with open("data/extended_apispecs_documentation.json", "r") as f:
            dict = json.load(f)
            log.info(f"=== Opened EXTENDED API Specification ===")

            total_num = len(dict["documents"])

            # zipping together all 3 arrays from the JSON file + iterating
            for i, (j_document, j_id, j_metadatas) in enumerate(zip(dict["documents"],dict["ids"],dict["metadatas"])):
                # logging status
                log.info(f"Working on {i} out of {total_num} ({j_id}).")

                document_chunks = self._chunk_text(j_document,2048)

                # create for each document chunk ids. Use operationId as base id.
                ids = [f"{j_id}_{x}" for x in range(len(document_chunks))]

                # create metadata for each document chunk
                metadatas = [j_metadatas for x in range(len(document_chunks))]

                #logging chunks
                #log.debug(document_chunks)

                # === put all information into vectorDB ===

                # add into vectordb
                self.database.collection_add(
                    documents=document_chunks,
                    ids=ids,
                    metadatas=metadatas
                )

        log.info(f"=== Chunked and embedded the openapi specification into the vectorDB ===")

    
    
    def _chunk_text(self,content,chunk_size):
        """
        The most basic method: Chunking by characters
        + Replacing the new line character with a white space
        + Removing any leading and trailing whitespaces

        Args:
            content (str): string to chunk
            chunk_size (int): number of characters when to 
            
        Return:
            Chunks (dict)
        """
        chunks = [content[i:i + chunk_size].replace("\n"," ").strip() for i in range(0, len(content), chunk_size)]
        return chunks