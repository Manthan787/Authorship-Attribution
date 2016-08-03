from elasticsearch import Elasticsearch, helpers
from config import *


es = Elasticsearch()

def createIndex():
    """ Creates Index

    :return: Void
    """
    res = es.indices.create(index=INDEX, body=ES_SETTINGS)
    print "Index creation Response %s" %res


def deleteIndex():
    """ Deletes the Index if it exists
    :return: Void
    """
    if es.indices.exists(INDEX):
        print "Deleting '%s' index" % (INDEX)
        response = es.indices.delete(index = INDEX)
        print "Deletion Response %s" %(response)


def index(docs):
    """
    :param docs: A dictionary containing document ID as key and document properties
                 as value
    :return: Void
    """
    print "Bulk indexing all %s texts" %(len(docs))
    helpers.bulk(es, action(docs))
    print "Done Indexing!"


def action(docs):
    """
    :param docs: Dictionary containing Document ID as key and its properties as value
    :return: Dict
    """
    for docno, properties in docs.iteritems():
        yield({'_index': INDEX, '_type': TYPE, '_id': docno, '_source': properties})