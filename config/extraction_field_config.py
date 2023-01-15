class Schema:
    
    def __init__(self) -> None:
        pass

    def Mappings():

        datasource = {
            "name":str,
            "url":str,
            "slug":str,
            "dateOfPublication":"date",
            "lastUpdatedAt":"date"
        }

        category = {
            "id":int,
            "name":str,
            "slug":str
        }

        sentiment = {
            "compound":float,
            "polarity": {"neutral":float, "positive":float, "negative":float}
        }

        author = {
            "name":str,
            "image":str,
            "description":str
        }

        named_entities = {
            "name":str,
            "image":str,
            "description":str
        }

        details = {
            "title":str,
            "summary":str,
            "dateGenerated":"date",
            "datasource":datasource,
            "category":category,
            "sentiment":sentiment,
            "keywords":list,
            "author":author,
            "image":str,
            "named_entities":named_entities, # list of dict
            "raw_text":str
        }
        return {
            "guid":str,
            "details":details
        }