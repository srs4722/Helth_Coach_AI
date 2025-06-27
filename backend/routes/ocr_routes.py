from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

# Create a Blueprint for OCR routes
ocr_routes = Blueprint("ocr_routes", __name__)

# Define allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload image for OCR
@ocr_routes.route("/upload", methods=["POST"])
def upload_image():
    # Check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    # If no file is selected or the filename is empty
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        # Secure the file name to prevent directory traversal
        filename = secure_filename(file.filename)

        # Save the file (here we just save it to a temporary directory for now)
        upload_folder = "uploads"  # Define your upload folder
        os.makedirs(upload_folder, exist_ok=True)  # Create the folder if it doesn't exist
        file_path = os.path.join(upload_folder, filename)
        
        # Save the file
        file.save(file_path)

        # Perform OCR (Placeholder, integrate actual OCR processing here)
        # You can integrate Tesseract or other OCR libraries here
        ocr_result = "OCR processing result will go here."

        # Return a success response with the OCR result (dummy result for now)
        return jsonify({
            "message": "File uploaded successfully!",
            "file_path": file_path,
            "ocr_result": ocr_result
        }), 200

    # If the file is not allowed, return an error
    return jsonify({"error": "Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed."}), 400
