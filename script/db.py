"""_summary_
"""
import urllib.parse
from pymongo import MongoClient
from pymongo.server_api import ServerApi

user = urllib.parse.quote_plus("amrsanubtc")
password = urllib.parse.quote_plus("kite@123")
uri = f"mongodb+srv://{user}:{password}@kite-db.jtrmqlf.mongodb.net/?appName=kite-db"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['kite']
users_collection = db['kite-user']

