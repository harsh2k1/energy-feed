import spacy
from nltk.tokenize import word_tokenize
import re
nlp = spacy.load("en_core_web_sm")

def NER(text: str):
    sentences = [sent for sent in nlp(text.replace("\xa0","").strip()).sents if not re.search("\d+",text)]
    new_sent = []
    for sent in sentences:
        a = ' '.join([token.text for token in sent if not token.is_stop and token.pos_ != 'PUNCT'])
        new_sent.append(a)
    
    d = dict([(str(x), x.label_) for x in nlp(str(new_sent)).ents])
    entities = list(set([k.strip("'") for k,v in d.items() if len(word_tokenize(k))>1 and (v=='ORG' or v == 'PERSON')]))
    entities = [{"name":entity} for entity in entities]

    return entities