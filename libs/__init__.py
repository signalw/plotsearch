import nltk
from elasticsearch import Elasticsearch
from search_engine import SearchEngine

try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except Exception as e:
    nltk.download("averaged_perceptron_tagger")
try:
    nltk.data.find("tokenizers/punkt")
except Exception as e:
    nltk.download("punkt")
try:
    nltk.data.find("corpora/stopwords")
except Exception as e:
    nltk.download("stopwords")

INDEX, TYPE = "plotsearch", "movie"
se = SearchEngine(Elasticsearch(), INDEX, TYPE)
