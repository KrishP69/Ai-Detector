from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from detector import detect_ai

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return "AI Detector API Running"


@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(path)

    result = detect_ai(path)

    os.remove(path)

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)