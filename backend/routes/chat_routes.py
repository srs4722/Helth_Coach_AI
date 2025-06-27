from flask import Blueprint, request, jsonify
from config import Config  # Make sure this has your GEMINI_API_KEY
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        logger.debug(f"Received chat request: {data}")
        
        message = data.get('message')
        if not message:
            logger.warning("No message provided in request")
            return jsonify({"error": "Message is required"}), 400

        # Use latest working model
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro-latest",  # Updated model name
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )

        system_instruction = "You are a health coach providing advice on fitness, diet, and nutrition."
        prompt = f"{system_instruction} {message}"
        logger.debug(f"Sending request to Gemini API: Prompt={prompt}")

        response = model.generate_content(prompt)
        logger.debug(f"Gemini API response: {response.text}")
        return jsonify({"response": response.text})

    except genai.types.BlockedPromptException as e:
        logger.error(f"Prompt blocked by Gemini API: {str(e)}")
        return jsonify({"error": "Prompt was blocked due to safety concerns. Please rephrase your message."}), 400

    except genai.errors.NotFound as e:
        logger.error(f"Model not found: {str(e)}")
        return jsonify({"error": "The requested AI model is not available. Please contact support."}), 404

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
