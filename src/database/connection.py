from pymongo import MongoClient

from config import settings


client = MongoClient(settings.mongo_uri)

db = client[settings.database_name]

earthquakes_collection = db["earthquakes"]
metrics_collection = db["metrics"]
hourly_reports_collection = db["hourly_reports"]