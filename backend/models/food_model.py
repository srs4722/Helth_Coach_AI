from config import MONGO_URI, DB_NAME
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
food_logs = db["food_logs"]

def log_food(user_email, food_text):
    food_logs.insert_one({"email": user_email, "food": food_text})

def get_food_logs(user_email):
    return list(food_logs.find({"email": user_email}, {"_id": 0}))
