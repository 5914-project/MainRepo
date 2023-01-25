from elasticsearch import Elasticsearch, helpers
import os, re, glob, json

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


def index():
    files = []

    os.chdir("recipes_by_food")
    
    for file in glob.glob("*.json"):
        f = open(file)
        data = json.load(f)
        files.append(data)

    return files

index()