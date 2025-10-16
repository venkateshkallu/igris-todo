import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(mongo_uri)
    db.database = db.client.kirotasks
    print("Connected to MongoDB")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")

def get_database():
    return db.database