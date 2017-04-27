from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

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
        """Search match_all for now.
        """
        query = form.get("query")
        rtmin, rtmax = form.get("rtmin"), form.get("rtmax")
        runtime = {}
        if rtmin: runtime["gte"] = int(rtmin)
        if rtmax: runtime["lte"] = int(rtmax)
        s = Search(using=self.client, index=self.index,
            doc_type=self.doc_type).query(Q("match", Plot=query)) \
            .filter("range", Runtime=runtime)
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
