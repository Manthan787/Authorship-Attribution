# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from config import TTF_BODY, INDEX, TYPE
import sys
import json


es = Elasticsearch(timeout=1000)


def get_ttf(term_df):
    print "Getting TTF From Index"
    i = 0
    for term in term_df:
        i += 1
        sys.stdout.write("Progress: %d \r" %i)
        sys.stdout.flush()
        ttf_body = TTF_BODY.format(term)
        res = es.search(index=INDEX, doc_type=TYPE, body=ttf_body)
        hits = res['hits']['hits']
        term_df[term].append(hits[0]['fields']['ttf'][0])

    return term_df


def get_freq_terms():
    print "Getting vocabulary from the Index!"
    termDocFreq = {}
    res = es.search(index=INDEX, doc_type=TYPE, search_type="count",
                    body={"aggs":{"unique_terms":{"terms":{"field":"text", "size":2147483647}}}})

    for i, row in enumerate(res['aggregations']['unique_terms']['buckets']):
        termDocFreq[row['key']] = [float(row['doc_count'])]
        sys.stdout.write("Progress: %d \r" %i)
        sys.stdout.flush()
        # print token.encode('utf-8','ignore'), str(termDocFreq.get(token)).encode('utf-8','ignore')

    return termDocFreq


if __name__ == '__main__':
    term_df = get_freq_terms()
    term_ttf = get_ttf(term_df)
    print "Writing Term_TTF to file!"
    with open("term_ttf", 'w') as f:
        json.dump(term_ttf, f)