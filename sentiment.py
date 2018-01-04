import string
import numpy as np
import pandas as pd
import json
import nltk
import csv

# nltk.download()

p = string.punctuation
d = string.digits
table_p = str.maketrans(p, len(p) * " ")
table_d = str.maketrans(d, len(d) * " ")
stopwords = nltk.corpus.stopwords.words("english")
columns = ['Place', 'State', 'City', 'Status']
tweet = pd.DataFrame(columns=columns)
place = []
state = []
city = []
status = dict()
text = []
tweet_score = dict()
# stopwords = nltk.download('stopwords')
txt_file = r"C:/Users/srinivas venkatesh/Documents/data science/assignments/assg2/data/AFINN-111.txt"
csv_file = r"C:/Users/srinivas venkatesh/Documents/data science/assignments/assg2/data/AFINN-111.csv"
#in_txt = csv.reader(open(txt_file, "r"), delimiter = '\t')
#out_csv = csv.writer(open(csv_file, 'w', newline=''))
#out_csv.writerows(in_txt)
#out_csv.close()

scores = {}
with open(csv_file) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            k = row[0]
            v = row[1]
            v = float(v)
            scores[k] = v


def preprocess(status):
    status_lower = status.lower()
    status_text_p = status_lower.translate(table_p)
    status_text_pd = status_text_p.translate(table_p)
    status_words = nltk.word_tokenize(status_text_pd)
    status_words = [w for w in status_words if w not in stopwords]
    return status_words


def getSentiment(words):
    result = 0.0
    for word in words:
        if word in scores:
            result = result + scores[word]
    return result


with open("C:/Users/srinivas venkatesh/Documents/data science/assignments/assg2/data/data.json", 'r') as fp:
    obj = json.load(fp)
for i in range(len(obj)):

    if 'place' in obj[i]:
        if obj[i]['place'] != None:
            if obj[i]['place']['country'] == 'United States':
                status_text = obj[i]["text"]
                word_list = preprocess(status_text)
                p = str(obj[i]['place']['full_name'])
                if obj[i]['place']['full_name'] not in status.keys():
                    status[p] = word_list
                else:
                    status[p] = status[p] + word_list


for k, v in status.items():
    tweet_score[k] = getSentiment(v)


states_abbrevation = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
state_score = dict()


def populate(key, value):
    if key not in status.keys():
        state_score[key] = value
    else:
        state_score[key] = int(state_score[key]) + int(value)

for k, v in tweet_score.items():
    if k != 'United States':
        str1,str2 = k.split(',')

        str2 = str2.strip()
        if str2 in states_abbrevation.keys():
            populate(str2,v)
        elif str1 in states_abbrevation.values():
            for key,value in states_abbrevation.items():
                if value == str1:
                    populate(key,v)

print(len(state_score))
print('state:  sentiment')
for k, v in state_score.items():
    print(k+":      "+str(v))
