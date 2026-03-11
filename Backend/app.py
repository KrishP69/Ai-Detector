from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------
# EDGE ANALYSIS
# -----------------------

def edge_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    density = np.sum(edges) / (img.shape[0] * img.shape[1])

    return min(100, density * 80)


# -----------------------
# TEXTURE ANALYSIS
# -----------------------

def texture_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap = cv2.Laplacian(gray, cv2.CV_64F)

    variance = lap.var()

    return min(100, variance / 25)


# -----------------------
# LIGHTING ANALYSIS
# -----------------------

def lighting_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mean = np.mean(gray)
    std = np.std(gray)

    ratio = std / (mean + 1)

    return min(100, ratio * 60)


# -----------------------
# SENSOR NOISE ANALYSIS
# -----------------------

def noise_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    noise = cv2.absdiff(gray, blur)

    level = np.mean(noise)

    return min(100, level * 4)


# -----------------------
# DETECT ENDPOINT
# -----------------------

@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error":"No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = cv2.imread(path)

    edge = edge_score(img)
    texture = texture_score(img)
    lighting = lighting_score(img)
    noise = noise_score(img)

    # Balanced scoring

    ai_score = (
        edge * 0.15 +
        texture * 0.20 +
        lighting * 0.15 +
        noise * 0.50
    )

    ai_score = round(min(ai_score,100),2)

    # Higher threshold reduces false positives

    if ai_score > 80:
        label = "AI Generated"
    else:
        label = "Likely Real"

    return jsonify({
        "result": label,
        "confidence": ai_score,
        "pattern": round(edge,2),
        "lighting": round(lighting,2),
        "texture": round(texture,2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)