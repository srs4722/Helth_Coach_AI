from flask import Blueprint, request, jsonify
from db import mongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from bson.objectid import ObjectId
from models.user_model import save_user_full_profile, get_user_full_profile  # Updated absolute import

# ------------------ Config ------------------ #
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")

user_routes = Blueprint("user_routes", __name__)

# ------------------ Token Required Decorator ------------------ #
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"_id": ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({"error": "User not found"}), 401
        except:
            return jsonify({"error": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# ------------------ Register Route ------------------ #
@user_routes.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        print("Received data:", data)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            print("Missing fields")
            return jsonify({"error": "Please provide all fields"}), 400

        if "@" not in email or "." not in email:
            print("Invalid email format")
            return jsonify({"error": "Invalid email format"}), 400

        existing_user = mongo.db.users.find_one({"email": email})
        print("Existing user:", existing_user)

        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.datetime.utcnow()
        }

        result = mongo.db.users.insert_one(user_data)
        print("Inserted ID:", result.inserted_id)

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print("Registration error:", e)
        return jsonify({"error": "Registration failed"}), 500

# ------------------ Login Route ------------------ #
@user_routes.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Please provide email and password"}), 400

        user = mongo.db.users.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid email or password"}), 400

        token = jwt.encode(
            {"user_id": str(user["_id"]), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            JWT_SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({"message": "Login successful!", "token": token}), 200

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Login failed"}), 500

# ------------------ Logout Route ------------------ #
@user_routes.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful!"}), 200

# ------------------ Save Profile Route ------------------ #
@user_routes.route("/profile", methods=["POST"])
@token_required
def save_profile(current_user):
    try:
        profile_data = request.get_json()
        user_id = ObjectId(current_user["_id"])
        if save_user_full_profile(user_id, profile_data):
            return jsonify({"message": "Profile saved successfully!"}), 200
        return jsonify({"error": "Failed to save profile"}), 500
    except Exception as e:
        print("Profile save error:", e)
        return jsonify({"error": "Failed to save profile"}), 500

# ------------------ Get Profile Route ------------------ #
@user_routes.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    try:
        user_id = ObjectId(current_user["_id"])
        profile = get_user_full_profile(user_id)
        return jsonify(profile), 200
    except Exception as e:
        print("Profile fetch error:", e)
        return jsonify({"error": "Failed to fetch profile"}), 500