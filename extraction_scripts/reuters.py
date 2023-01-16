import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class ExtractData:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_soup(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    def get_data(self):
        counter=0
        while True:
            try:
                url = f'https://www.reuters.com/site-search/?query=renewable+energy&offset={counter}'
                soup = self.get_soup(url)
                print(soup.prettify())
                data_secs = soup.find_all("div",{"class":"media-story-card__body__3tRWy"})
                break
                
                print(len(data_secs))
            except:
                break
            counter += 20

obj = ExtractData()
obj.get_data()