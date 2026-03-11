import requests
import os
import cv2
import numpy as np
from PIL import Image, ExifTags
from dotenv import load_dotenv

load_dotenv()

API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")


# ---------------- API Detection ---------------- #

def api_detection(image_path):

    url = "https://api.sightengine.com/1.0/check.json"

    files = {'media': open(image_path, 'rb')}

    data = {
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }

    response = requests.post(url, files=files, data=data)

    result = response.json()

    try:
        score = result["type"]["ai_generated"] * 100
    except:
        score = 0

    return score


# ---------------- Metadata Analysis ---------------- #

def metadata_score(image_path):

    try:
        img = Image.open(image_path)
        exif = img._getexif()

        if exif is None:
            return 70

        tags = {}

        for tag, value in exif.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            tags[decoded] = value

        if "Model" in tags or "Make" in tags:
            return 10

        return 40

    except:
        return 50


# ---------------- Texture Analysis ---------------- #

def texture_score(image_path):

    try:
        img = cv2.imread(image_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        laplacian = cv2.Laplacian(gray, cv2.CV_64F)

        variance = laplacian.var()

        if variance < 60:
            return 65

        return 20

    except:
        return 30


# ---------------- Noise Analysis ---------------- #

def noise_score(image_path):

    try:
        img = cv2.imread(image_path, 0)

        noise = np.std(img)

        if noise < 25:
            return 60

        return 15

    except:
        return 30


# ---------------- Forensic Image Generation ---------------- #

def generate_forensic_image(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)

    forensic = cv2.addWeighted(img, 0.7, heatmap, 0.3, 0)

    output_path = "uploads/forensic.jpg"

    cv2.imwrite(output_path, forensic)

    return output_path


# ---------------- Final Score ---------------- #

def final_score(api, meta, texture, noise):

    score = (
        api * 0.5 +
        meta * 0.2 +
        texture * 0.2 +
        noise * 0.1
    )

    return round(score, 2)


# ---------------- Main Detection ---------------- #

def detect_ai(image_path):

    api = api_detection(image_path)
    meta = metadata_score(image_path)
    texture = texture_score(image_path)
    noise = noise_score(image_path)

    final = final_score(api, meta, texture, noise)

    forensic_path = generate_forensic_image(image_path)

    result = "AI Generated" if final > 50 else "Likely Real"

    return {
        "result": result,
        "confidence": final,
        "api_score": round(api, 2),
        "metadata_score": meta,
        "texture_score": texture,
        "noise_score": noise,
        "forensic_image": "/forensic"
    }