from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
import nltk

class SearchEngine(object):
    """A class for searching movies in corpus with
    elasticsearch.
    """

    def __init__(self, client, index, doc_type):
        """Initialize metadata.
        """
        super(SearchEngine, self).__init__()
        self.client = client
        self.index = index
        self.doc_type = doc_type

    def search(self, form, start, end):
        """Process query and search relevant movies.
        """
        query = form.get("query")
        token_tags = nltk.pos_tag(nltk.word_tokenize(query))
        keywords = [token for token, tag in token_tags if \
            tag.startswith("NN") or \
            tag.startswith("VB") or \
            tag.startswith("PRP") or \
            tag.startswith("JJ") or \
            tag.startswith("RB")]
        rtmin, rtmax = form.get("rtmin"), form.get("rtmax")
        runtime = {}
        if rtmin: runtime["gte"] = int(rtmin)
        if rtmax: runtime["lte"] = int(rtmax)
        s = Search(using=self.client, index=self.index,
            doc_type=self.doc_type).query(Q("match_phrase",
            Plot={"query": ' '.join(keywords), "slop": 50})) \
            .filter("range", Runtime=runtime)
        language = form.get("language")
        if language: s = s.filter("match", Language=language)
        s = s[start:end]
        res = s.execute()
        return res

    def search_by_id(self, id):
        """Retrieve a document by id.
        """
        s = Search(using=self.client, index=self.index,
            doc_type=self.doc_type).query("term", _id=id)
        res = s.execute()
        return res[0] if res else None
