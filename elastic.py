from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

def search(query):
    es.indices.refresh(index="page")    
    res = es.search(index="page", q=query)
    return res
