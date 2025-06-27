from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo  # Import the mongo instance from db.py

# ------------------ Create User ------------------ #
def create_user(username, email, password, age, height, weight):
    if mongo.db.users.find_one({"email": email}):
        return None  # User already exists

    hashed_password = generate_password_hash(password)

    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "age": age,
        "height": height,
        "weight": weight
    }

    mongo.db.users.insert_one(user_data)
    
    # Exclude password from the returned data for security
    user_data.pop("password", None)
    return user_data


# ------------------ Find User by Email ------------------ #
def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})


# ------------------ Authenticate User ------------------ #
def authenticate_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        # Return user data excluding password for security
        user_data = {key: value for key, value in user.items() if key != "password"}
        return user_data
    return None


# ------------------ Update User Profile ------------------ #
def update_user_profile(user_id, username=None, age=None, height=None, weight=None):
    update_fields = {}
    if username is not None:
        update_fields["username"] = username
    if age is not None:
        update_fields["age"] = age
    if height is not None:
        update_fields["height"] = height
    if weight is not None:
        update_fields["weight"] = weight

    if not update_fields:
        return False  # Nothing to update

    result = mongo.db.users.update_one({"_id": user_id}, {"$set": update_fields})
    return result.modified_count > 0


# ------------------ Save Full Profile ------------------ #
def save_user_full_profile(user_id, profile_data):
    result = mongo.db.users.update_one(
        {"_id": user_id},
        {"$set": {"profile": profile_data}}
    )
    return result.modified_count > 0


# ------------------ Get Full Profile ------------------ #
def get_user_full_profile(user_id):
    user = mongo.db.users.find_one({"_id": user_id}, {"profile": 1, "_id": 0})
    return user.get("profile", {}) if user else {}