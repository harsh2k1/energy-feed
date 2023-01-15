import sys
sys.path.append("./")
from extraction_scripts.greentech_media import ExtractData

class Extraction:

    def __init__(self) -> None:
        pass

    @staticmethod
    def greentech_media():
        obj = ExtractData(category={
            "id":1,
            "name":'Solar Energy',
            "slug":'solar-energy'
        }, url='https://www.greentechmedia.com/channel/solar', filename= 'data_dump/solar-data.json')
        obj.get_data()

        obj = ExtractData(category={
            "id":2,
            "name":'Grid Edge',
            "slug":'grid-edge'
        }, url='https://www.greentechmedia.com/channel/gridedge', filename= 'data_dump/greentech-gridedge-data.json')
        obj.get_data()

        obj = ExtractData(category={
            "id":3,
            "name":'Wind Energy',
            "slug":'wind-energy'
        }, url='https://www.greentechmedia.com/articles/category/wind', filename= 'data_dump/greentech-wind-data.json')
        obj.get_data()

        obj = ExtractData(category={
            "id":4,
            "name":'Podcast',
            "slug":'podcast'
        }, url='https://www.greentechmedia.com/podcast/the-energy-gang', filename= 'data_dump/podcast-energygang-data.json')
        obj.get_data()

        obj = ExtractData(category={
            "id":4,
            "name":'Podcast',
            "slug":'podcast'
        }, url='https://www.greentechmedia.com/podcast/the-interchange', filename= 'data_dump/podcast-interchange-data.json')
        obj.get_data()


if __name__ == "__main__":
    obj = Extraction()
    obj.greentech_media()