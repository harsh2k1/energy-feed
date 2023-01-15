import sys
sys.path.append('./')
from services.config_services import config
from services.elasticSearch import ElasticSearch
import os
import json

def load_json(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())
    return data

def de_loading():
    counter = 0
    for file in os.listdir(config['PATH']['project_path']+'/data_dump'):
        data = load_json(f'{config["PATH"]["project_path"]}/data_dump/{file}')
        print(len(data))
        for data_point in data:
            es_obj = ElasticSearch()
            es_obj.addRecord(data=data_point)
            counter += 1

            if counter%100 == 0:
                print("Number of Records added: ", counter)

if __name__ == "__main__":
    de_loading()

