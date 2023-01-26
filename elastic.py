from elasticsearch import Elasticsearch, helpers
from es_utility import get_data
import re

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
es = Elasticsearch(es_header)


print(es)

query_body = {
  "query": {
    "match": {
      'title': 'fried chicken'
    }
  }
}

res = es.search(index="recipes", body=query_body, size=1000)
print(len(res["hits"]["hits"]))
for doc in res["hits"]["hits"]:
  print(doc)

''' uncomment to create index and add json data to index '''
# es.indices.create(index = 'recipes')
# result = helpers.bulk(es, get_data('recipes', 'recipes_by_food'), request_timeout=60*3)

''' delete the index '''
# es.indices.delete(index='recipes', ignore=[400, 404])