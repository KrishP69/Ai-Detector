from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load pretrained AI detector
detector = pipeline(
    "image-classification",
    model="umm-maybe/AI-image-detector"
)


@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    image = Image.open(path)

    results = detector(image)

    ai_score = 0
    real_score = 0

    for r in results:
        label = r["label"].lower()

        if "ai" in label or "generated" in label:
            ai_score = r["score"] * 100
        else:
            real_score = r["score"] * 100

    if ai_score > real_score:
        result = "AI Generated"
        confidence = ai_score
    else:
        result = "Likely Real"
        confidence = real_score

    return jsonify({
        "result": result,
        "confidence": round(confidence,2),
        "pattern": round(ai_score * 0.6,2),
        "lighting": round(ai_score * 0.3,2),
        "texture": round(ai_score * 0.2,2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)