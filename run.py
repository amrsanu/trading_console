import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

user = urllib.parse.quote_plus("amrsanubtc")
password = urllib.parse.quote_plus("kite@123")
uri = f"mongodb+srv://{user}:{password}@kite-db.jtrmqlf.mongodb.net/?appName=kite-db"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['kite']

collection = db['kite-user']
document = collection.find_one()

print("Single document:", document)
documents = collection.find()
for doc in documents:
    print(doc)
