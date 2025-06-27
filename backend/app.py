import sys
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from db import init_db, mongo
from routes.user_routes import user_routes
from routes.chat_routes import chat_bp
from routes.food_routes import food_routes
from routes.ocr_routes import ocr_routes
from routes.workout_routes import workout_routes  # Add this import
from config import Config  # Import Config from the same directory

# -------------------- Add backend directory to Python path -------------------- #
# Ensure the parent directory (backend/) is in the Python path for relative imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# -------------------- Debug Environment Variables -------------------- #
# Fetch environment variables (print for debugging purposes)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: GEMINI_API_KEY from environment: {GEMINI_API_KEY}")

# -------------------- Flask App Setup -------------------- #
app = Flask(__name__, static_folder="../frontend", static_url_path='')
app.secret_key = Config.SECRET_KEY  # Set secret key for session security

# -------------------- Load Configuration -------------------- #
app.config.from_object(Config)

# -------------------- MongoDB Configuration -------------------- #
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/healthcoach")
with app.app_context():
    init_db(app)

# -------------------- Check MongoDB Connection -------------------- #
try:
    with app.app_context():
        if mongo.db is None:
            raise RuntimeError("mongo.db is None after initialization")
        mongo.db.command("ping")
    print(" MongoDB connection successful")
except Exception as e:
    print(" MongoDB connection failed:", e)
    exit(1)

# -------------------- CORS Configuration -------------------- #
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Restrict to API routes for security

# -------------------- Register API Blueprints -------------------- #
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(food_routes, url_prefix="/api/food")
app.register_blueprint(ocr_routes, url_prefix="/api/ocr")
app.register_blueprint(workout_routes, url_prefix="/api/workouts")  # Add this line

# -------------------- Serve Frontend Static Files -------------------- #
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/favicon.ico")
def favicon():
    return '', 204

# -------------------- Debug Info -------------------- #
print("Registered Routes:")
for rule in app.url_map.iter_rules():
    methods = ','.join(rule.methods) if rule.methods else 'N/A'
    print(f"{rule} (Methods: {methods})")

# -------------------- Gemini API Key Check -------------------- #
# Check if GEMINI_API_KEY is present in the environment variables
if not GEMINI_API_KEY:
    print(" WARNING: GEMINI_API_KEY is not set. Chat functionality may fail.")
else:
    print("Gemini API Key is set successfully.")

# -------------------- Run Server -------------------- #
if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)