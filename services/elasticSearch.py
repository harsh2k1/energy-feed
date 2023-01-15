from elasticsearch import Elasticsearch
import sys
sys.path.append("./")
from services.config_services import config

es = Elasticsearch(
    hosts=config['ES']['host'] + ':' + config['ES']['port'],
    ca_certs=config['ES']['ca_cert'],
    basic_auth=config['ES']['authorization']
)

class ElasticSearch:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def addRecord(data, index=config['ES']['prod_index']):
        es.index(index=index, id=data["guid"], body=data)
        # print(f"Record added. Guid: {data['guid']}")

    @staticmethod
    def updateRecord(data,guid, index=config['ES']['prod_index']):
        es.index(index=index, id=guid, body=data)
        print(f"Updated Record. Guid: {guid}")

    # def deleteRecord
    @staticmethod
    def fetchRecord(body, index=config['ES']['prod_index']):
        res = es.search(index=index, body=body)
        res = res['hits']['hits'][0]
        return res

    

# Inserting data

doc_1 = {
    "guid":"test",
    "details":[{
        "author":{
            "name":"author1",
            "description":"demo author created"
        },
        "category":{
            "id":1,
            "name":"Green Energy",
            "slug":"green-energy"
        },
        "datasource":{
            "dateOfPublication":"2023-01-01T00:00:00.000Z",
            "name":"Green Technica",
            "slug":"green-technica",
            "url":"https://www.greentechnica.com"
        },
        "title":"demo title 1",
        "summary":"demo summary 1"
    }]
}
