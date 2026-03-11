from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import os
import random

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
FORENSIC_FOLDER = "forensic"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FORENSIC_FOLDER, exist_ok=True)


# -------------------------------
# Image Analysis Functions
# -------------------------------

def analyze_edges(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    edge_density = np.sum(edges) / (img.shape[0] * img.shape[1])

    score = min(100, edge_density * 400)

    return score


def analyze_texture(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap = cv2.Laplacian(gray, cv2.CV_64F)

    variance = lap.var()

    score = min(100, variance / 5)

    return score


def analyze_lighting(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mean = np.mean(gray)

    std = np.std(gray)

    ratio = std / (mean + 1)

    score = min(100, ratio * 120)

    return score


# -------------------------------
# Forensic Image Generator
# -------------------------------

def generate_forensic(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 80, 200)

    heat = cv2.applyColorMap(edges, cv2.COLORMAP_JET)

    blended = cv2.addWeighted(img, 0.6, heat, 0.4, 0)

    return blended


# -------------------------------
# Detection Endpoint
# -------------------------------

@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = cv2.imread(path)

    # Run analysis
    pattern_score = analyze_edges(img)
    lighting_score = analyze_lighting(img)
    texture_score = analyze_texture(img)

    # Final AI probability
    ai_score = (pattern_score * 0.4 +
                lighting_score * 0.3 +
                texture_score * 0.3)

    ai_score = round(ai_score, 2)

    if ai_score > 55:
        label = "AI Generated"
    else:
        label = "Likely Real"

    # Generate forensic map
    forensic = generate_forensic(img)

    forensic_path = os.path.join(FORENSIC_FOLDER, "forensic.jpg")

    cv2.imwrite(forensic_path, forensic)

    return jsonify({

        "result": label,
        "confidence": ai_score,

        "pattern": round(pattern_score,2),
        "lighting": round(lighting_score,2),
        "texture": round(texture_score,2)

    })


# -------------------------------
# Forensic Image Endpoint
# -------------------------------

@app.route("/forensic")
def forensic():

    return send_file("forensic/forensic.jpg", mimetype="image/jpeg")


# -------------------------------
# Run Server
# -------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)