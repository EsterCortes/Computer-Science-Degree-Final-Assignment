import pymongo
import json

conex = pymongo.MongoClient()

db = conex.dblp
col = db.documents

with open("dblp.json",'r') as f:
    my_json= json.load(f)

documents = my_json["dblp"]

for doc in documents:
    col.insert(doc)


