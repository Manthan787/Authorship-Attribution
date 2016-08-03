DATASET_PATH = '/Users/admin/Documents/NLP/Research/Blogger/blogs'

# File name components
DOCID = 0
GENDER = 1
AGE = 2
LIWC = 3

# Elastic search config
INDEX = 'blogger'
TYPE  = 'blog'
ES_SETTINGS = """{
  "settings": {
    "index": {
      "store": {
        "type": "default"
      },
      "max_result_window": 85000,
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "my_english": {
          "type": "custom",
          "tokenizer": "standard",
          "stopwords_path": "stoplist.txt",
          "filter": [
            "lowercase"
          ]
        }
      }
    }
  },
  "mappings": {
    "document": {
      "properties": {
        "docno": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        },
        "text": {
          "type": "string",
          "store": true,
          "index": "analyzed",
          "term_vector": "with_positions_offsets_payloads",
          "analyzer": "my_english"
        },
        "pronouns": {
          "type": "long",
          "store": true,
          "index": "not_analyzed"
        },
        "prepositions": {
          "type": "long",
          "store": true,
          "index": "not_analyzed"
        },
        "determiners": {
          "type": "long",
          "store": true,
          "index": "not_analyzed"
        },
        "gender": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        },
        "age": {
          "type": "integer",
          "store": true,
          "index": "not_analyzed"
        },
        "LIWC": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        }
      }
    }
  }
}"""
