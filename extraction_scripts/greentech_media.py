import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil import parser
import dateparser
from tqdm import tqdm
import sys
sys.path.append("./")
from services.guid_generator import get_guid

class ExtractData:
    def __init__(self, category, url, filename) -> None:
        self.datasource = {
            "name":'Greentech Media',
            "url":url,
            "slug":'greentech-media',
            "lastUpdatedAt":"date"
        }
        self.category = category
        self.url = url
        self.filename = filename

    @staticmethod
    def get_soup(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    @staticmethod
    def to_json(filename,data):
        with open(filename,"w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def date_parse(data):
        iso_date = dateparser.parse(data)
        data = iso_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
        data = data[:-3]+"Z"
        return data


    def extract_article(self,data_sec):
        data_dict = {}
        name = ''
        img = ''
        raw_text = ''
        lastUpdatedAt = ''
        author = {}
        keywords = []

        link = ''
        try:
            link = 'https://www.greentechmedia.com' + data_sec.find("div",{'class':'article-detail'}).find("a")['href']
        except:
            pass
        
        if not link:
            try:
                link = 'https://www.greentechmedia.com' + data_sec.find("a")['href']
            except:
                pass

        soup = self.get_soup(link)

        name = soup.find("h1",{"class":"article-page-heading"}).text.strip()
        
        img = 'https://www.greentechmedia.com' + soup.find("div",{'class':'media-holder'}).find("img")['src'][1:]

        temp = soup.find("span",{"class":"article-author"}).text.strip()
        if temp:
            author['name'] = temp

        temp = soup.find("span",{'class':'article-date'}).text.strip()
        if temp:
            lastUpdatedAt = self.date_parse(temp)
            self.datasource['lastUpdatedAt'] = lastUpdatedAt

        data_ps = soup.find("article").find_all("p")
        raw_text = ' '.join(ele.text.strip() for ele in data_ps if ele.text.strip() and '***' not in ele.text.strip())

        keys = soup.find("ul",{'class':'tag-list'}).find_all("li")
        keywords = [ele.text.strip() for ele in keys if ele.text.strip()]
        
        if raw_text:
            data_dict['title'] = name.strip()
            if img:
                data_dict['image'] = img.strip()
            if raw_text:
                data_dict['raw_text'] = raw_text.strip()
            if author:
                data_dict['author'] = author
            if self.datasource:
                data_dict['datasource'] = self.datasource
            if self.category:
                data_dict['category'] = self.category
            if keywords:
                data_dict['keywords'] = keywords

            data_dict['dateGenerated'] = datetime.now().isoformat()

        return data_dict

    def get_data(self):
        url = self.url
        urls = []
        data_list = []
        soup = self.get_soup(url)

        pages = soup.find("ul",{'class':"pagination"}).find_all("a")
        urls = [ele['href'] for ele in pages]

        for page in urls:
            soup = self.get_soup(page)
            data_secs = soup.find_all("article",{"class":"article-item clearfix"})
            for data_sec in tqdm(data_secs):
                final_dict = {}
                try:
                    data_dict = self.extract_article(data_sec)
                    if data_dict:
                        guid = get_guid(data_dict)
                        if guid:
                            final_dict = {"guid":guid, "details":[data_dict]}
                            data_list.append(final_dict)
                        # print(data_dict)
                except:
                    pass

        self.to_json(filename=self.filename, data=data_list)


# obj = ExtractData(category={
#             "id":1,
#             "name":'Solar Energy',
#             "slug":'solar-energy'
#         }, url='https://www.greentechmedia.com/channel/solar')
# obj.get_data()

