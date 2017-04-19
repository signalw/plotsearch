from elasticsearch import Elasticsearch
from search_engine import SearchEngine

INDEX, TYPE = "plotsearch", "movie"
se = SearchEngine(Elasticsearch(), INDEX, TYPE)
