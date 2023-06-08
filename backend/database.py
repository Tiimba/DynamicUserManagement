from pymongo import MongoClient
from misc import loadAndReadDBConfig


db_config_data = loadAndReadDBConfig()

hostname, port, username, password = db_config_data.get("hostname"), db_config_data.get("port"), db_config_data.get("username"), db_config_data.get("password")
def connectToDB():
    mongo_url = f"mongodb://{hostname}:{port}"
    client = MongoClient(mongo_url)
    db = client.dumdb
    for i in db.list_collection_names():
        print(i)


connectToDB()