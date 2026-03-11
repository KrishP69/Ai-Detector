from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import detect_ai

app = Flask(__name__)
CORS(app)

@app.route("/detect", methods=["POST"])

def detect():

    image = request.files["image"]

    label, score = detect_ai(image)

    return jsonify({
        "result": label,
        "confidence": round(score*100,2)
    })

if __name__ == "__main__":
  import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)