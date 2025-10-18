import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from flask import Flask, render_template, request
from PIL import Image
import os

# Flask app
app = Flask(__name__)

# Classes
class_names = ["Mild Dementia", "Moderate Dementia", "Non Demented", "Very mild Dementia"]

# Load model
DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = models.resnet101(weights=None)   # same architecture as training
model.fc = nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(
    torch.load("model/resnet101_extraData_5epochs.pth", map_location=DEVICE, weights_only=False)
)

model.to(DEVICE)
model.eval()

# Image transforms (use the same as training)
weights=models.ResNet101_Weights.IMAGENET1K_V1
transform = weights.transforms()

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]

        if file.filename == "":
            return "No file selected", 400

        # Save and preprocess
        img = Image.open(file.stream).convert("RGB")
        img_t = transform(img).unsqueeze(0).to(DEVICE)

        # Prediction
        with torch.no_grad():
            outputs = model(img_t)
            _, pred = torch.max(outputs, 1)
            prediction = class_names[pred.item()]

        return render_template("index.html", prediction=prediction, filename=file.filename)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

