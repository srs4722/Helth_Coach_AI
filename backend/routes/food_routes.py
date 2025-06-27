from flask import Blueprint, request, jsonify
from db import mongo  # Use the Flask-PyMongo instance from db.py
import logging
import datetime  # Added missing import for datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a Blueprint for food routes
food_routes = Blueprint("food_routes", __name__)

# Route to log food
@food_routes.route("/log", methods=["POST"])
def log_food():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        logger.debug(f"Received food log data: {data}")

        # Validate required fields
        required_fields = ["date", "mealType", "foodItem", "quantity", "unit", "calories"]
        if not data or not all(field in data for field in required_fields):
            missing = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        # Extract and prepare data
        food_data = {
            "email": data.get("email", "anonymous"),  # Optional: Add user email if authenticated
            "date": data.get("date"),
            "mealType": data.get("mealType"),
            "foodItem": data.get("foodItem"),
            "quantity": data.get("quantity"),
            "unit": data.get("unit"),
            "calories": data.get("calories"),
            "protein": data.get("protein", 0),  # Optional fields with defaults
            "carbs": data.get("carbs", 0),
            "fats": data.get("fats", 0),
            "notes": data.get("notes", ""),
            "timestamp": datetime.datetime.utcnow()  # Add server-side timestamp
        }

        # Insert into MongoDB
        result = mongo.db.food_logs.insert_one(food_data)
        logger.debug(f"Inserted food log with ID: {result.inserted_id}")

        # Respond with success and the logged data
        return jsonify({
            "message": "Food logged successfully!",
            "data": {key: value for key, value in food_data.items() if key != "_id"}
        }), 201

    except Exception as e:
        logger.error(f"Error logging food: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500