from elasticsearch import Elasticsearch, helpers
from flask import session
from Databases.es_utility import get_data
from Databases.models import User
import re, os

ES = None
INDEX = 'recipes'

def initialize():
    global ES

    #bonsai = os.environ.get('BONSAI_URL')
    bonsai = 'https://n6cfbimamd:esj58h0n5t@5914-search-2656906543.us-east-1.bonsaisearch.net:443'
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

    res = ES.search(index=INDEX, body=query_body, size=20)

    recipes = []
    for doc in res['hits']['hits']:
        recipe = {
           'id': doc['_id'],
           'title': doc['_source']['title'],
           'ingredients': [x.replace('ADVERTISEMENT', '') for x in doc['_source']['ingredients']],
           'instructions': doc['_source']['instructions'],
           'likes': doc['_source']['likes'],
           'liked': User().liked(doc['_id'])
        }
        recipes.append(recipe)

        print(recipe)
        print()

    return sorted(recipes, key=lambda d: d['likes'], reverse=True)


def get_recipes(ids):
    recipes = []

    for id in ids:
        result = ES.get(index=INDEX, id=id)
        recipe = {
            'id': result['_id'],
           'title': result['_source']['title'],
           'ingredients': [x.replace('ADVERTISEMENT', '') for x in result['_source']['ingredients']],
           'instructions': result['_source']['instructions'],
           'likes': result['_source']['likes'],
           'liked': User().liked(result['_id'])
        }
        recipes.append(recipe)

    return recipes


def update_likes(id, count):
   ES.update(
      index=INDEX,
      id=id,
      body={
        'doc': {'likes': count}
      }
    )
   

# creates index and add json data to index, do not call before deleting the index first
def index():
    ES.indices.create(index = INDEX)
    return helpers.bulk(ES, get_data(INDEX, '../recipes_by_food'), request_timeout=60*3)

# delete the index
def delete(index):
    ES.indices.delete(index=index, ignore=[400, 404])

