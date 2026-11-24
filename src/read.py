import json
import os
from filter import _match_filter

def read(table_name: str):
    file_path = f"data/{table_name}.json"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as file:
        return json.load(file)
    
def find(table_name: str, query: dict = None):
    documents = read(table_name)
    return [doc for doc in documents if _match_filter(doc, query)]

def findOne(table_name: str, query: dict = None):
    documents = read(table_name)
    for doc in documents:
        if _match_filter(doc, query):
            return doc
    return None