from pymongo import MongoClient



client = MongoClient("mongodb+srv://eidyunda:unda123@cluster0.haapq.mongodb.net/?retryWrites=true&w=majority")
conn = client.test

collection_name=conn["user"]

