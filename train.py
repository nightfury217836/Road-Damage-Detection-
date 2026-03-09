from ultralytics import YOLO
import torch

# -----------------------------
# Check device
# -----------------------------
device = "cpu"

print("Using device:", device)
print("Torch CUDA available:", torch.cuda.is_available())

# -----------------------------
# Load pretrained model
# -----------------------------
# Options: n < s < m < l < x
model = YOLO("yolo11n.pt")   # nano model 

# -----------------------------
# Train on CPU
# -----------------------------
model.train(
    data="data.yaml",   # dataset config
    epochs=100,          
    imgsz=640,          # keep ≤ 640 for CPU
    batch=4,            # lower batch for RAM safety
    device=device,      # force CPU
    workers=2,          # reduce CPU thread load
    cache=False,        # disable RAM caching 
    pretrained=True,   # use transfer learning
    optimizer="SGD",   # lighter on CPU than AdamW
    verbose=True
)
