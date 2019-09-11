from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from searchapp import models

# Create a connection to ElasticSearch
connections.create_connection()

class MarkedUrlIndex(DocType):
    user = Text()
    url = Text()
    title = Text()
    created_at = Date()


    class Meta:
        index = 'blogpost-index'

# Bulk indexing function, run in shell
def bulk_indexing():
    import pdb
    pdb.set_trace()
    MarkedUrlIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.MarkedUrl.objects.all().iterator()))

# Simple search function
def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response


if __name__ == "__main__":
    bulk_indexing()