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

    def search(self):
        """Search match_all for now.
        """
        s = Search(using=self.client, index=self.index,
            doc_type=self.doc_type).query(Q("match_all"))
        res = s.execute()
        return res

    def search_by_id(self, id):
        """Retrieve a document by id.
        """
        s = Search(using=self.client, index=self.index,
            doc_type=self.doc_type).query("term", _id=id)
        res = s.execute()
        return res[0] if res else None
