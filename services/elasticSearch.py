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
    def fetchRecord(body, index=config['ES']['prod_index'], scroll="20m", scrolling=True, size=1000):
        # def indexFetch(host:str, index:str, auth:str, body:dict, size:int=100, scroll = "20m", scrolling:bool = True) -> tuple:
        
        res = es.search(
                    query = body,
                    scroll =scroll,
                    size = size,
                    index = index,
                    request_timeout=40,
                )
        
        counter = 0 
        sid =  res["_scroll_id"]
        scroll_size = res['hits']['total']['value']
        
        data = res["hits"]["hits"]
        sidList = []
        sidList.append(sid)
        if scrolling:
            while (scroll_size > 0):
                page = es.scroll(scroll_id = sid, scroll = scroll)
                sid = page['_scroll_id']
                sidList.append(sid)
                scroll_size = len(page['hits']['hits'])
                data+=page["hits"]["hits"]
                counter = counter + 1

        es.clear_scroll(scroll_id=sidList)
        return data, counter

    
if __name__ == "__main__":
    import json
    import sys
    from tqdm import tqdm
    sys.path.append("./")
    from services.guid_generator import get_guid
    with open("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/data_dump/clean-technica.json","r") as f:
        new_records = json.loads(f.read())
    
    for record in tqdm(new_records[1:]):
        new_record = {}
        guid = get_guid(record)
        new_record['guid'] = guid
        new_record['details'] = [record]
        es_obj = ElasticSearch()
        es_obj.addRecord(new_record)
        # break
        