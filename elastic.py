from elasticsearch import Elasticsearch, helpers
from es_utility import get_data
import re

ES = None

def initialize():
    global ES

    # bonsai = os.environ['BONSAI_URL']
    bonsai = 'https://aheh650jci:y2gh5o7eb0@student-search-6074912715.us-east-1.bonsaisearch.net:443'
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    # optional port
    match = re.search('(:\d+)', host)
    if match:
      p = match.group(0)
      host = host.replace(p, '')
      port = int(p.split(':')[1])
    else:
      port=443

    # Connect to cluster over SSL using auth for best security:
    es_header = [{
    'host': host,
    'port': port,
    'use_ssl': True,
    'http_auth': (auth[0],auth[1])
    }]

    # Instantiate the new Elasticsearch connection:
    ES = Elasticsearch(es_header)

    print(ES)




def search(ingredients, title=''):

    query_body1 = {
       'query': {
            'bool': {
                'must' : {
                    'match': {
                        'title' : title
                    }
                },
                'should' : {
                    "multi_match" : {
                        "query":    ingredients, 
                        "fields": [ 'ingredients' ] 
                    }
                }
            }
       }
    }

    query_body = {
        "query": {
            "multi_match" : {
                "query":    ingredients, 
                "fields": [ 'ingredients' ] 
            }
        }
    }
    
    res = ES.search(index="recipes", body=query_body, size=10)
    
    for doc in res["hits"]["hits"]:
        print(doc)
        print()

    print(len(res["hits"]["hits"]))

    return res['hits']['hits']


# initialize()
# search('green onion pepper', 'soup')


# creates index and add json data to index, do not call before deleting the index first
def index():
    ES.indices.create(index = 'recipes')
    return helpers.bulk(ES, get_data('recipes', 'recipes_by_food'), request_timeout=60*3)

# delete the index
def delete():
    ES.indices.delete(index='recipes', ignore=[400, 404])
