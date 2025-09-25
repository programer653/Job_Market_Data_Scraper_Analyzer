import pandas as pd 
import string
import re 
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


#nltk.download() 

df = pd.read_csv("./data/raw_jobs.csv")
stop_words = set(stopwords.words('english'))

def clean(text):
    
    # lowercase
    text = text.lower()

    # replace
    punctuation_to_remove = string.punctuation.replace("#", "").replace("+", "")
    text = re.sub(f"[{re.escape(punctuation_to_remove)}]", " ", text)
    
    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # tokenize
    tokens = word_tokenize(text)

    # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    #tokens = text.apply( lambda x: [word for word in word_tokenize(x) if word not in stop_words])

    return tokens

def run_cleaner():
    df['tokens'] = df['description'].astype(str).apply(clean)
    df.to_csv('./data/clean_jobs.csv', index=False)
    #print(df) # debug

#run_cleaner()


#run_cleaner()

#df['token'] = df['description']

# remove extra spaces
#df['description'] = df['description'].str.replace(r"\s+", " ", regex=True).str.strip()


#remove stop words

#df['description'] = df['description'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
#df['token'] = df['description'].apply( lambda x: [word for word in word_tokenize(x) if word not in stop_words])
#df['description'] = word_tokenize(str(df['description']))