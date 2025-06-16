from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

mongo_uri=os.getenv("Mongo_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "idea_vault")

client=MongoClient(mongo_uri)
db=client[MONGO_DB_NAME]

users_collection = db["users"]
ideas_collection = db["ideas"]