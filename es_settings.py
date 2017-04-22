"""
This script creates an index and a type, and loads
corpus into elasticsearch.
Change constants accordingly to modify ES datatype.
Make sure ES is running before executing.
"""
import json, re, time
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Mapping, Nested

##########
# CONFIG #
##########
JSON_FILE = "data/movie_corpus.json"
INDEX = "plotsearch"
TYPE = "movie"
FIELDS = [
    ("Ratings", (("Source", "text"), ("Value", "text"))),
    ("Rated", "text"),
    ("Plot", "text"),
    ("DVD", "date"),
    ("Writer", "text"),
    ("Production", "text"),
    ("Actors", "text"),
    ("Type", "text"),
    ("imdbVotes", "integer"),
    ("Website", "text"),
    ("Poster", "text"),
    ("Title", "text"),
    ("Director", "text"),
    ("Released", "date"),
    ("Awards", "text"),
    ("Genre", "text"),
    ("imdbRating", "float"),
    ('Language', 'text'),
    ("Country", "text"),
    ("BoxOffice", "text"),
    ("Runtime", "integer"),
    ("imdbID", "text"),
    ("Metascore", "integer"),
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
def normalize_date(string):
    if not string or string == "N/A": return
    t = time.strptime(string, "%d %b %Y")
    return "-".join(["%d" % t.tm_year, "%02d" % t.tm_mon, "%02d" % t.tm_mday])

def normalize_year(string):
    if string: return string[:4]

def normalize_imdbrating(string):
    if string != "N/A": return string

def normalize_strtlist(string):
    return [i.strip() for i in string.split(",")]

def normalize_digits(string):
    if string and string != "N/A": return string.replace(",", "")

def normalize_runtime(string):
    if string and string != "N/A": return string.strip(" min")

FIELDS_TO_NORMALIZE = [
    (normalize_date, ["DVD", "Released"]),
    (normalize_year, ["Year"]),
    (normalize_imdbrating, ["imdbRating"]),
    (normalize_strtlist, ["Writer", "Actors", "Genre", "Country", "Language"]),
    (normalize_digits, ["imdbVotes", "Metascore"]),
    (normalize_runtime, ["Runtime"]),
]

with open(JSON_FILE) as f:
    d = json.load(f)

for k in d:
    for normalize, fields in FIELDS_TO_NORMALIZE:
        for field in fields:
            d[k][field] = normalize(d[k].get(field))

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
