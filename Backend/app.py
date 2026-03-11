from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------
# Load pretrained model
# ---------------------------

model = torch.hub.load(
    "pytorch/vision",
    "resnet18",
    pretrained=True
)

model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

# ---------------------------
# Forensic heuristics
# ---------------------------

def edge_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray,80,200)

    density = np.sum(edges)/(img.shape[0]*img.shape[1])

    return min(100,density*80)


def texture_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap = cv2.Laplacian(gray,cv2.CV_64F)

    return min(100,lap.var()/20)


def noise_score(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    noise = cv2.absdiff(gray,blur)

    return min(100,np.mean(noise)*3)


# ---------------------------
# Deep model prediction
# ---------------------------

def ai_probability(image):

    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)

    probs = torch.nn.functional.softmax(output,dim=1)

    # entropy approximation
    entropy = -torch.sum(probs*torch.log(probs))

    ai_score = float(entropy*15)

    return min(100,ai_score)


# ---------------------------
# Detection endpoint
# ---------------------------

@app.route("/detect",methods=["POST"])
def detect():

    if "image" not in request.files:
        return jsonify({"error":"No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER,file.filename)
    file.save(path)

    pil_img = Image.open(path).convert("RGB")
    cv_img = cv2.imread(path)

    deep_score = ai_probability(pil_img)

    e = edge_score(cv_img)
    t = texture_score(cv_img)
    n = noise_score(cv_img)

    # combined score
    ai_score = (
        deep_score*0.6 +
        e*0.15 +
        t*0.15 +
        n*0.10
    )

    ai_score = round(min(ai_score,100),2)

    if ai_score > 75:
        label = "AI Generated"
    else:
        label = "Likely Real"

    return jsonify({
        "result":label,
        "confidence":ai_score,
        "pattern":round(e,2),
        "texture":round(t,2),
        "noise":round(n,2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)