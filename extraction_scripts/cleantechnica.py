import requests
from bs4 import BeautifulSoup
import yake
import sys
from tqdm import tqdm
sys.path.append("./")
from src.features.features_main import Features
import dateparser
import json
import warnings
warnings.filterwarnings("ignore")
import traceback

class ExtractData:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_soup(url):
        header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3" ,
            'referer':'https://cleantechnica.com/'
        }
        res = requests.get(url, headers=header)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    @staticmethod
    def date_parse(data):
        iso_date = dateparser.parse(data)
        data = iso_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
        data = data[:-3]+"Z"
        return data

    def extract_article(self,data_sec):
        data_dict = {}
        link = data_sec.find("a")['href']
        soup = self.get_soup(link)
        title = soup.find("h1",{'class':'zox-post-title left entry-title'}).text.replace("amp;","").strip()
        img = ''
        author = {}
        try:
            img = soup.find("div",{'class':'zox-post-img left zoxrel zoxlh0'}).find("img")['src']
        except:
            pass
        
        try:
            author_name = soup.find("span",{'class':'zox-author-box-name zoxrel'}).text.strip()
            if author_name:
                author['name'] = author_name
            author_desc = soup.find("div",{'class':'zox-author-box-text left zoxrel'}).text.strip().replace("\n"," ")
            if author_desc:
                author['description'] = author_desc
            author_img = soup.find("img",{'class':'avatar avatar-150 photo'})['src']
            if author_img:
                author['image'] = author_img
        except:
            pass

        raw_text = ''
        data_ps = soup.find("div",{'class':'zox-post-body left zoxrel zox100'}).find_all("p")
        raw_text = ' '.join([ele.text.strip() for ele in data_ps if ele.text.strip()])
        kw_extractor = yake.KeywordExtractor(top=50, stopwords=None)
        keywords = kw_extractor.extract_keywords(raw_text)
        
        keywords2 = []
        for kw, v in keywords:
            keywords2.append(kw)
    

        obj = Features()
        summary = obj.extractSummary(raw_text)
        sentiment = obj.extractSentiment(raw_text)
        try:
            named_entities = obj.extractNE(raw_text)
        except:
            pass
        category = {
            "id": 5,
            "name":"Clean Energy",
            "slug":"clean-energy"
        }
        datasource = {
            "name":'Clean Technica',
            "url":link,
            "slug":'clean-technica',
            "lastUpdatedAt":self.date_parse("17 January 2023")
        }

        if title:
            data_dict['title'] = title
            if img:
                data_dict['image'] = img
            if raw_text:
                data_dict['raw_text'] = raw_text
            if summary:
                data_dict['summary'] = summary
            if datasource:
                data_dict['datasource'] = datasource
            if category:
                data_dict['category'] = category
            if named_entities:
                data_dict['named_entities'] = named_entities
            if sentiment:
                data_dict['sentiment'] = sentiment
            if keywords2:
                data_dict['keywords'] = keywords2
            if author:
                data_dict['author'] = author
            
        return data_dict
        

    def get_data(self):
        # for i in range()
        data_list = []
        url = 'https://cleantechnica.com/page/1/'
        soup = self.get_soup(url)
        
        pages = soup.find("div",{'class':'pagination'}).find("span").text.split("of")[-1].strip()
        
        for page in tqdm(range(1, int(pages))):
            try:
                url = f'https://cleantechnica.com/page/{page}/'
                soup = self.get_soup(url)
                data_secs = soup.find_all("div",{'class':'zox-art-title'})

                for data_sec in data_secs:
                    try:
                        data_dict = self.extract_article(data_sec)
                        if data_dict:
                            data_list.append(data_dict)
            
                    except Exception as e:
                        error = traceback.format_exception(type(e), e, e.__traceback__)
                        print(error)
                        pass
                    # break

            except:
                pass
            # break

            with open("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/data_dump/clean-technica.json","w") as f:
                f.write(json.dumps(data_list))
            

obj = ExtractData()
obj.get_data()

