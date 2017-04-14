import json, requests
import temp # place where raw plot data are stored

corpus = {}
for title, plot in temp.data:
    meta = requests.get("http://www.omdbapi.com/?t=%s" % title).json()
    if meta["Response"] == "False": continue
    imdbID = meta["imdbID"]
    meta["Plot"] = plot
    corpus[imdbID] = meta

with open("data/toy_corpus.json", "w") as f:
    json.dump(corpus, f, indent=4)
