from flask import Blueprint, request, jsonify
from models.workout_model import log_workout, get_workouts
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

workout_routes = Blueprint("workout_routes", __name__)

@workout_routes.route("/log", methods=["POST"])
def log_workout_entry():
    try:
        data = request.get_json()
        logger.debug(f"Received workout log data: {data}")

        required_fields = ["exercise", "sets", "reps", "duration"]
        if not data or not all(field in data for field in required_fields):
            missing = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        user_email = data.get("email", "anonymous")
        workout_data = log_workout(
            user_email=user_email,
            exercise=data.get("exercise"),
            sets=data.get("sets"),
            reps=data.get("reps"),
            duration=data.get("duration")
        )

        return jsonify({
            "message": "Workout logged successfully!",
            "data": workout_data
        }), 201

    except Exception as e:
        logger.error(f"Error logging workout: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@workout_routes.route("/log", methods=["GET"])
def get_workout_logs():
    try:
        email = request.args.get("email", "anonymous")
        workouts = get_workouts(email)
        return jsonify(workouts), 200
    except Exception as e:
        logger.error(f"Error retrieving workouts: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500