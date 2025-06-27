from db import mongo
import datetime

def log_workout(user_email, exercise, sets, reps, duration):
    workout_data = {
        "email": user_email,
        "exercise": exercise,
        "sets": int(sets),
        "reps": int(reps),
        "duration": int(duration),
        "timestamp": datetime.datetime.utcnow()
    }
    result = mongo.db.workouts.insert_one(workout_data)
    workout_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return workout_data

def get_workouts(user_email):
    return list(mongo.db.workouts.find({"email": user_email}, {"_id": 0}))  # Exclude _id