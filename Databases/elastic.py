from elasticsearch import Elasticsearch, helpers
from Databases.es_utility import get_data
import re, os

ES = None

def initialize():
    global ES

    bonsai = os.environ.get('BONSAI_URL')
    print(os.environ.get('MONGODB'))
    print(os.environ.get('RAPIDAPI_KEY'))
    print(bonsai)
   
    # bonsai = 'https://n6cfbimamd:esj58h0n5t@5914-search-2656906543.us-east-1.bonsaisearch.net:443'
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




def search(ingredients):
    query_body = {
       'query': {
            'bool': {
                'should': [{'match_phrase': {'ingredients': x}} for x in ingredients]
            }
       }
    }

    res = ES.search(index="recipes", body=query_body, size=10)

    recipes = []
    for doc in res['hits']['hits']:
        recipe ={
           'title': doc['_source']['title'],
           'ingredients': [x.replace('ADVERTISEMENT', '') for x in doc['_source']['ingredients']],
           'instructions': doc['_source']['instructions']
        }
        recipes.append(recipe)

        print(doc)
        print()

    return recipes

# initialize()
# search(['chicken', 'green onion', 'rice'])

# creates index and add json data to index, do not call before deleting the index first
def index():
    ES.indices.create(index = 'recipes')
    return helpers.bulk(ES, get_data('recipes', '../recipes_by_food'), request_timeout=60*3)

# delete the index
def delete(index):
    ES.indices.delete(index=index, ignore=[400, 404])

