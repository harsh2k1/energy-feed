import torch
from transformers import AutoTokenizer, AutoModelWithLMHead, T5Tokenizer, TFT5ForConditionalGeneration
import sys
import json
sys.path.append("./")
from services.elasticSearch import ElasticSearch
from src.features.keyword_extraction import TextRank4Keyword
from src.features.summarization import summary_generator
from src.features.sentiments import sentiment_analysis
from src.features.named_entity_recognition import NER
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained('t5-base')
model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

class Features:
    
    def __init__(self) -> None:
        # self.entity = entity
        self.data = []
        self.updated_records = []
    
    @staticmethod
    def extractKeywords(text: str) -> list:
        kw_obj = TextRank4Keyword()
        keywords = kw_obj.extract_keywords(text, size=50)
        return keywords

    @staticmethod
    def extractSummary(text: str) -> str:
        summary = summary_generator(tokenizer,model,text)
        return summary

    @staticmethod
    def extractSentiment(text: str) -> dict:
        sent = sentiment_analysis(text)
        return sent

    @staticmethod
    def extractNE(text:str) -> dict:
        entities = NER(text)
        return entities

    def commonUtility(self, status='f'):
        es_obj = ElasticSearch()

        if status == 'f':
            body = {
                    "bool":{
                        "must":[
                            {
                                "exists":{
                                    "field":"guid"
                                }
                            }
                        ]
                    }
                }
            self.data, _ = es_obj.fetchRecord(body=body)
        
        elif status == 'u':
            for data in self.updated_records:
                es_obj.updateRecord(data=data, guid=data['guid'])


    def get_features(self):
        print("Fetching Records...")
        self.commonUtility()

        data_list = []
        for data_ in tqdm(self.data[1:]):
            # print("Done\nExtracting Keywords...")
            keywords = self.extractKeywords(text=data_['_source']['details'][0]['raw_text'])
            # print("Done\nExtracting Summary...")
            summary = self.extractSummary(text=data_['_source']['details'][0]['raw_text'])
            # print("Done\nExtracting Sentiment...")
            sentiment = self.extractSentiment(text=data_['_source']['details'][0]['raw_text'])
            # print("Done\nExtracting Named Entities...")
            entities = self.extractNE(text=data_['_source']['details'][0]['raw_text'])

            data_['_source']['details'][0]['keywords'] = keywords
            data_['_source']['details'][0]['summary'] = summary
            data_['_source']['details'][0]['sentiment'] = sentiment
            data_['_source']['details'][0]['named_entities'] = entities
            data_list.append(data_['_source'])

            with open("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/data_dump/updated_records.json","w") as f:
                f.write(json.dumps(data_list))

        print("Done\nSaving Records")
        with open("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/data_dump/updated_records.json","w") as f:
            f.write(json.dumps(data_list))

if __name__ == "__main__":
    obj = Features()
    obj.get_features()
    

