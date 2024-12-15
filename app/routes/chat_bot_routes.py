import logging
import json
import re
from flask import Blueprint, jsonify, request
from ..config import Config
import google.generativeai as genai

# Initialize logging
logging.basicConfig(level=logging.ERROR)

chat_bot_bp = Blueprint('chat_bot', __name__)

# Configure the GenAI API key
genai.configure(api_key=Config.GEMINI_API_KEY)


def is_disaster_related(prompt):
    disaster_keywords = [
        "disaster", "catastrophe", "flood", "earthquake", "hurricane", "tornado",
        "tsunami", "wildfire", "volcano", "landslide", "avalanche", "storm",
        "drought", "epidemic", "pandemic", "emergency", "natural disaster",
        "evacuation", "rescue", "relief", "hazard", "crisis"
    ]
    pattern = re.compile(
        r'\b(' + '|'.join(disaster_keywords) + r')\b', re.IGNORECASE)
    return bool(pattern.search(prompt))


def generate_sources(response_text):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )

        # Use triple quotes to properly handle multi-line strings
        prompt = (
            f"Generate 3 links, and only links (no additional information) "
            f"based on the following text:\n\n{response_text}\n\n"
            f"Return the links in the following format: ['Source 1', 'Source 2', 'Source 3']"
        )

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [prompt],
                }
            ]
        )

        response = chat_session.send_message(
            f"Generate 3 links related to the following content: {response_text}"
        )

        sources = eval(response.text.strip())

        return sources
    except Exception as e:
        print("Error generating sources:", e)
        return []


@chat_bot_bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    prompt = data.get("prompt", "")
    return_sources = data.get("returnSources", True)
    return_follow_up_questions = data.get("returnFollowUpQuestions", True)

    try:

        chat_session = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        ).start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [prompt],
                }
            ]
        )

        response = chat_session.send_message(prompt)
        answer = response.text

        response_obj = {"answer": answer}

        if return_sources:
            response_obj["sources"] = generate_sources(answer)

        return jsonify(response_obj), 200

    except Exception as e:
        print("Error in fetching or generating response:", e)
        return jsonify({"error": "Internal Server Error"}), 500
