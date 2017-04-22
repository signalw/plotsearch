"""
This script collects movie plots and its metadata
from websites and save the corpus as a json file.
"""
from bs4 import BeautifulSoup
import json, re, requests

cands, corpus = [], {}

r = requests.get("http://www.themoviespoiler.com/Pages/Spoilers.html").text
soup = BeautifulSoup(r, "html.parser")
tables = soup.find_all("table")
for table in tables:
    links = table.find_all("a")
    for link in links:
        if re.match(r"\.\.\/Spoilers\/\w+\.html", link["href"]):
            url = "http://www.themoviespoiler.com%s" % link["href"].strip(".")
            title = link.text
            if title.endswith(", The"): title = "The "+title[:-5]
            cands.append((url, title))

for url, title in cands:
    r = requests.get(url).text
    soup = BeautifulSoup(r, "html.parser")
    paragraphs = soup.find_all("p")
    plot = '\n'.join([p.text for p in paragraphs])
    plot = re.sub(r".*?\s*NOTE:.*\s*|" + \
        r"\W*CUT TO THE CHASE\W*|" + \
        r"\W*Brought to you by\W*|" + \
        r"[\s\_]*You can send in your spoiler[\s\w\W]*|" + \
        r"\t+",
        "", plot
    )
    try:
        meta = requests.get("http://www.omdbapi.com/?t=%s" % title).json()
        assert meta["Response"] == "True"
    except:
        print "Fail to get metadata for %s" % title
        continue
    imdbID = meta["imdbID"]
    meta["Plot"] = plot
    corpus[imdbID] = meta

print "%d movie plots collected." % len(corpus)

with open("data/movie_corpus.json", "w") as f:
    json.dump(corpus, f, indent=4)
