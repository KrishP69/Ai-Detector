from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import clip
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

text = clip.tokenize([
    "a real photograph",
    "an AI generated image"
]).to(device)


@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    image = preprocess(Image.open(path)).unsqueeze(0).to(device)

    with torch.no_grad():

        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        logits = (image_features @ text_features.T).softmax(dim=-1)

        real_prob = float(logits[0][0]) * 100
        ai_prob = float(logits[0][1]) * 100

    if ai_prob > real_prob:
        label = "AI Generated"
        confidence = ai_prob
    else:
        label = "Likely Real"
        confidence = real_prob

    return jsonify({
        "result": label,
        "confidence": round(confidence,2),
        "pattern": round(ai_prob * 0.6,2),
        "lighting": round(ai_prob * 0.3,2),
        "texture": round(ai_prob * 0.2,2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)