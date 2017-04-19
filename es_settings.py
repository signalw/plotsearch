"""
This script creates an index and a type, and loads
corpus into elasticsearch.
Change constants accordingly to modify ES datatype.
Make sure ES is running before executing.
"""
import json
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Mapping, Nested

##########
# CONFIG #
##########
JSON_FILE = "data/toy_corpus.json"
INDEX = "plotsearch"
TYPE = "movie"
FIELDS = [
    # may suppress cases
    ("Ratings", (("Source", "text"), ("Value", "text"))),
    ("Rated", "text"),
    ("Plot", "text"),
    ("DVD", "text"), # can be date, need preprocessing "1 Jan 1999"
    ("Writer", "text"), # can be list, need preprocessing "A, B, C"
    ("Production", "text"),
    ("Actors", "text"), # can be list, need preprocessing "A, B, C"
    ("Type", "text"),
    ("imdbVotes", "text"), # can be integer, need preprocessing "10,123"
    ("Website", "text"),
    ("Poster", "text"),
    ("Title", "text"),
    ("Director", "text"),
    ("Released", "text"), # can be date, need preprocessing "1 Jan 1999"
    ("Awards", "text"),
    ("Genre", "text"), # can be list, need preprocessing "A, B, C"
    ("imdbRating", "float"),
    ('Language', 'text'),
    ("Country", "text"), # can be list, need preprocessing "A, B, C"
    ("BoxOffice", "text"), # can be float, need preprocessing "$3,562,379.00"
    ("Runtime", "text"), # can be integer, need preprocessing "96 min"
    ("imdbID", "text"),
    ("Metascore", "text"), # can be integer, need handling "N/A"
    ("Response", "text"),
    ("Year", "date")
]

###########
# SETTING #
###########
connections.create_connection()
index = Index(INDEX)
index.delete(ignore=404)
index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)
index.create()
index.close()

###########
# MAPPING #
###########
m = Mapping(TYPE)
for f in FIELDS:
    if isinstance(f[1], tuple):
        n = Nested()
        for nf in f[1]: n.field(*nf)
        m.field(f[0], n)
    else:
        m.field(*f)
m.save(INDEX)
index.open()

#############
# LOAD DATA #
#############
with open(JSON_FILE) as f:
    d = json.load(f)
actions = [
    {
        "_index": INDEX,
        "_type": TYPE,
        "_id": k,
        "_source": v,
    }
    for k, v in d.items()
]
es = Elasticsearch()
helpers.bulk(es, actions)
