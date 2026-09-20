from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

client.admin.command("ping")

print("Conexión exitosa con MongoDB")