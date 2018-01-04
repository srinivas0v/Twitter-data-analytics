import numpy as np  # a conventional alias
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import nltk
from sklearn import decomposition
import json

p = string.punctuation
d = string.digits
table_p = str.maketrans(p, len(p) * " ")
table_d = str.maketrans(d, len(d) * " ")
stopwords = nltk.corpus.stopwords.words("english")

def preprocess(status):
    status_lower = status.lower()
    # print(status_lower)
    status_text_p = status_lower.translate(table_p)
    # print(status_text_p)
    status_text_pd = status_text_p.translate(table_p)
    # print(status_text_pd)
    status_words = nltk.word_tokenize(status_text_pd)
    # print(status_words)
    status_words = [w for w in status_words if w not in stopwords]
    # print(status_words)
    return status_words

topic_text = []
with open("C:/Users/srinivas venkatesh/Documents/data science/assignments/assg2/data/data.json", 'r') as fp:
    obj = json.load(fp)
for i in range(len(obj)):
    status = obj[i]["text"]
    preprocessed_status_words = preprocess(status)
    status_text = ' '.join( wrd for wrd in preprocessed_status_words)
    topic_text.append(status_text)



vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
dtm = vectorizer.fit_transform(topic_text)

num_topics = 10
num_top_words = 20
clf = decomposition.NMF(n_components = num_topics, random_state=1)
doctopic = clf.fit_transform(dtm)
topic_words = []
for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    topic_words.append([topic_text[i] for i in word_idx])



for t in range(len(topic_words)):
    print("Topic {}: {}".format(t, ' '.join(topic_words[t][:15])))

