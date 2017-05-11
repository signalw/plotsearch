"""
This script creates an index and a type, loads
corpus into elasticsearch, and configures synonym
file.

Change constants accordingly to modify ES datatype.
Make sure ES is running before executing.

Since it copies the synonym file into the default
config directory of elasticsearch, root access is
required.

Usage:
    $ sudo <virtualenv_dir>/bin/python es_settings.py
"""
import json, os, re, requests, shutil, time
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Mapping, Nested, analyzer

##########
# CONFIG #
##########
JSON_FILE = "data/movie_corpus.json"
INDEX = "plotsearch"
TYPE = "movie"
FIELDS = [
    ("Ratings", (("Source", "text"), ("Value", "text"))),
    ("Rated", "text"),
    ("Plot", "text", {"analyzer": "synonym"}),
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
# Copy synonym file into elasticsearch config directory
r = requests.get("http://localhost:9200/_nodes/settings")
def find_path(dic, key):
    if key in dic: return dic[key]
    for k, v in dic.items():
        if isinstance(v,dict):
            item = find_path(v, key)
            if item: return item
conf_path = find_path(r.json(), "conf")
analysis_path = os.path.join(conf_path, "analysis")
if os.path.exists(analysis_path):
    shutil.rmtree(analysis_path)
os.mkdir(analysis_path)
shutil.copy("data/wn_s.pl", analysis_path)
shutil.copy("data/names.txt", analysis_path)

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
index._analysis = {
    "analyzer": {
        "synonym": {
            "tokenizer": "whitespace",
            "filter": [
                "standard",
                "stop",
                "lowercase",
                "porter_stem",
                "synonym_wn",
                "synonym_prp"
            ]
        }
    },
    "filter": {
        "synonym_wn": {
            "type": "synonym",
            "format": "wordnet",
            "synonyms_path": "analysis/wn_s.pl"
        },
        "synonym_prp": {
            "type": "synonym",
            "synonyms_path": "analysis/names.txt"
        }
    }
}
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
    elif len(f) > 2:
        m.field(*f[:2], **f[2])
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
