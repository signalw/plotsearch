PlotSearch
============
An application to search for movies based on plot description. The user is provided with a text box where queries can be input in the form of sentences describing the scenes of what actually happened. Our system returns relevant movies that match the description.

### File structure

```
/
├───data
|    ├───movie_corpus.json  #main corpus file
|    ├───names.txt  #names to pronoun mapping file
|    ├───toy_corpus.json  #test corpus file
|    └───wn_s.pl  #wordnet synonyms file
├───doc
|    ├───PlotSearch.pdf
|    └───PlotSearch.tex
├───libs
|    ├───__init__.py
|    └───search_engine.py  #script for searching documents with elasticsearch
├───static
|    ├───images
|    |    └───background.jpg
|    ├───js
|    |    ├───bootstrap.min.js
|    |    ├───jquery.min.js
|    |    └───main.js
|    └───styles
|         ├───bootstrap.min.css
|         └───style.css
├───templates
|    ├───base.html
|    ├───index.html
|    ├───movie.html
|    └───results.html
├───app.py  # flask app main controller
├───create_corpus.py  #script for creating corpus
├───es_settings  # set up elasticsearch
├───README.md
└───requirements.txt
```

### Local Setup

To install dependencies:
```
pip install -r requirements
```

To create corpus from scratch:
```
python create_corpus.y
```

It will go to themoviespoiler.com and omdbapi.com, fetch and clean movie data, and save it to `data/movie_corpus.json`.

To build elasticsearch index (it copies synonym files into elasticsearch config directory, therefore root access is required):
```
sudo <virtualenv_dir>/bin/python es_settings.py
```

Then the flask application can be kicked off by running:
```
python app.py
```
