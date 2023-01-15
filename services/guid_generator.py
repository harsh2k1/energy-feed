
from unicodedata import normalize
import hashlib

def stringNormalization(text):
    """
    converting unicode characters of string
    """
    string_encode = normalize('NFKD', text).encode('ascii','ignore')
    return string_encode.decode()


def get_guid(data_dict):
    title = data_dict.get("title")
    datasource = data_dict.get("datasource")
    name, url = '', ''
    if datasource:
        name = datasource.get("slug")
        url = datasource.get("url")

    if title:
        title = stringNormalization(title)
    else:
        return None
    if name:
        name = stringNormalization(name)
    else:
        name = 'datasource name not present'
    if url:
        url = stringNormalization(url)
    else:
        url = 'datasource url not present'

    temp = title+name.strip()+url.strip()
    hash_obj = hashlib.sha256(temp.encode())
    temp = hash_obj.hexdigest()
    return (temp)

    