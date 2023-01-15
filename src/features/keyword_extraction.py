from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import os
import pandas as pd

nlp = spacy.load('en_core_web_sm')


class TextRank4Keyword():
    """Extract keywords from text"""
    
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight

    @staticmethod
    def set_stopwords(stopwords):  
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    @staticmethod
    def sentence_segment(doc, candidate_pos, lower,bigrams,trigrams):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)

            if bigrams==True:
                for i in range(len(sent)-1):
                    if sent[i].pos_ in candidate_pos and sent[i].is_stop is False and sent[i+1].pos_ in candidate_pos and sent[i+1].is_stop is False:
                        if lower is True:
                            selected_words.append(sent[i].text.lower())
                        else:
                            selected_words.append(str(sent[i].text+" "+sent[i+1].text))
            if trigrams==True:
                for i in range(len(sent)-2):
                    if sent[i].pos_ in candidate_pos and sent[i].is_stop is False and sent[i+1].pos_ in candidate_pos and sent[i+1].is_stop is False and sent[i+2].pos_ in candidate_pos and sent[i+2].is_stop is False:
                        if lower is True:
                            selected_words.append(sent[i].text.lower())
                        else:
                            selected_words.append(str(sent[i].text+" "+sent[i+1].text+" "+sent[i+2].text))

            sentences.append(selected_words)
        return sentences
    
    @staticmethod
    def get_vocab(sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    @staticmethod
    def get_token_pairs(window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
    
    @staticmethod
    def symmetrize(a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        """Print top number keywords"""
        # print(len(self.node_weight.items()))
        node_weight_list = [list(ele) for ele in self.node_weight.items()]
        for i in node_weight_list:
            res = len(i[0].split())
            if res==2:
                # weight for bigrams
                i[1]=4*i[1]
            if res==3:
                # weight for trigrams
                i[1]=6*i[1]

        node_weight = OrderedDict(sorted(node_weight_list, key=lambda t: t[1], reverse=True))
        data_list = []
        keywords = []
        for i, (key, value) in enumerate(node_weight.items()):
            # print(key + ' - ' + str(value))
            # data_list.append({
            #     "text":key,
            #     "relevance":value
            # })
            keywords.append(key)

            # print(i,':',key)
            if i > number:
                break
        
        # df = pd.DataFrame(data_list)
        # df.to_csv("keyword_output.csv",index=False)
        return keywords
        
    def analyze(self, text,
                candidate_pos=['NOUN', 'VERB'],
                window_size=4, lower=False,bigrams=False,trigrams=False, stopwords=list()):
        """Main function to analyze text"""

        # Set stop words
        self.set_stopwords(stopwords)

        # Pare text by spaCy
        doc = nlp(text)

        #
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower,bigrams,trigrams) # list of list of words

        # ences)
        # Build vocabulary
        vocab = self.get_vocab(sentences)


        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)


        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)


        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))


        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight

    def extract_keywords(self,text, size=10):
        self.analyze(text, candidate_pos=['NOUN','PROPN','VERB'], window_size=4, lower=False, bigrams=True, trigrams=True)
        keywords = self.get_keywords(size)
        return keywords


# if __name__ == "__main__":
    
#     import json
#     from tqdm import tqdm
#     with open("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/data_dump/raw_text.json","r") as f:
#         test_cases = json.loads(f.read())
    
#     data = []
#     for test_case in tqdm(test_cases):
#         obj = TextRank4Keyword()
#         keywords = obj.extract_keywords(test_case, size=50)
#         data.append({
#             "text":test_case,
#             "keywords":keywords
#         })

#     with open("/Users/harshpreetsingh/Documents/iit_madras_hackathon/repository/ns-python/data_dump/keywords.json","w") as f:
#         f.write(json.dumps(data))
