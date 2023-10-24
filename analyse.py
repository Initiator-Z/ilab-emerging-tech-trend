import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from domain import application_domains
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords.words('english')]
    return ' '.join(tokens)

def extract_keywords(publication_index, tfidf_matrix, tfidf_vectorizer, top_n=10):
    publication_tfidf = tfidf_matrix[publication_index].toarray().flatten()
    top_keywords_idx = np.argsort(publication_tfidf)[-top_n:][::-1]
    top_keywords = [tfidf_vectorizer.get_feature_names_out()[i] for i in top_keywords_idx]
    return top_keywords

def predict_class(dadaframe):
    df = dadaframe.dropna()

    df['processed_desc'] = df['description'].apply(preprocess_text)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['processed_desc'])
    df['keywords'] = df.index.map(lambda idx: extract_keywords(idx, tfidf_matrix, tfidf_vectorizer))
    df['keywords_str'] = df['keywords'].apply(lambda x: ' '.join(x))
    domain_keywords_str = [' '.join(keywords) for keywords in application_domains.values()]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(df['keywords_str'].tolist() + domain_keywords_str)
    keyword_tfidf = tfidf_vectorizer.transform(df['keywords_str'])
    domain_tfidf = tfidf_vectorizer.transform(domain_keywords_str)

    similarities = cosine_similarity(keyword_tfidf, domain_tfidf)
    classifications = [list(application_domains.keys())[sim.argmax()] for sim in similarities]
    df['classification'] = classifications

    return df
