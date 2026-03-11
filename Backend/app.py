from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
FORENSIC_FOLDER = "forensic"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FORENSIC_FOLDER, exist_ok=True)


# ---------------------------
# EDGE ANALYSIS
# ---------------------------

def analyze_edges(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    edge_density = np.sum(edges) / (img.shape[0] * img.shape[1])

    score = min(100, edge_density * 120)

    return score


# ---------------------------
# TEXTURE ANALYSIS
# ---------------------------

def analyze_texture(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap = cv2.Laplacian(gray, cv2.CV_64F)

    variance = lap.var()

    score = min(100, variance / 18)

    return score


# ---------------------------
# LIGHTING ANALYSIS
# ---------------------------

def analyze_lighting(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mean = np.mean(gray)
    std = np.std(gray)

    ratio = std / (mean + 1)

    score = min(100, ratio * 70)

    return score


# ---------------------------
# SENSOR NOISE ANALYSIS
# ---------------------------

def analyze_noise(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    noise = cv2.absdiff(gray, blur)

    noise_level = np.mean(noise)

    score = min(100, noise_level * 3)

    return score


# ---------------------------
# FORENSIC VISUALIZATION
# ---------------------------

def generate_forensic(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 80, 200)

    heat = cv2.applyColorMap(edges, cv2.COLORMAP_JET)

    forensic = cv2.addWeighted(img, 0.75, heat, 0.25, 0)

    return forensic


# ---------------------------
# DETECTION ENDPOINT
# ---------------------------

@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = cv2.imread(path)

    # Run analysis

    edge_score = analyze_edges(img)
    texture_score = analyze_texture(img)
    lighting_score = analyze_lighting(img)
    noise_score = analyze_noise(img)

    # Balanced scoring

    ai_score = (
        edge_score * 0.25 +
        texture_score * 0.25 +
        lighting_score * 0.25 +
        noise_score * 0.25
    )

    ai_score = ai_score * 1.15

    ai_score = round(min(ai_score, 100), 2)

    # Higher threshold reduces false positives

    if ai_score > 72:
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

        "pattern": round(edge_score,2),
        "lighting": round(lighting_score,2),
        "texture": round(texture_score,2),
        "noise": round(noise_score,2)

    })


# ---------------------------
# FORENSIC IMAGE ENDPOINT
# ---------------------------

@app.route("/forensic")
def forensic():

    return send_file("forensic/forensic.jpg", mimetype="image/jpeg")


# ---------------------------
# RUN SERVER
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)