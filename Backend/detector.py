import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")
import requests
import os

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

def detect_ai(image):

    response = requests.post(
        "https://api.sightengine.com/1.0/check.json",
        files={'media': image},
        data={
            'models': 'genai',
            'api_user': API_USER,
            'api_secret': API_SECRET
        }
    )

    result = response.json()

    score = result["type"]["ai_generated"]

    if score > 0.5:
        label = "AI Generated"
    else:
        label = "Likely Real"

    return label, score