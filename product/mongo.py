from pymongo import MongoClient
from django.conf import settings


def get_db_handle(db_name, port=27017):
    if settings.DEBUG:
        client = MongoClient(host=settings.MONGO_HOST, port=int(port))
    else:
        client = MongoClient(host=settings.MONGO_HOST)
    db_handle = client[db_name]
    return db_handle


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]
