# Import Libraries
from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import os
import uuid

# App Configuration
app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load YOLO Model
model = YOLO("best.pt")  # Ensure best.pt is in root folder


# Helper Function → Count Classes
def count_detections(results):

    counts = {
        "D00": 0,   # Longitudinal
        "D10": 0,   # Transverse
        "D20": 0,   # Alligator
        "D40": 0,   # Pothole
        "OTHER": 0
    }

    # CLASS NAME → CODE MAP
    class_map = {
        "Longitudinal Crack": "D00",
        "Transverse Crack": "D10",
        "Alligator Crack": "D20",
        "Potholes": "D40"  
    }

    for r in results:
        if r.boxes is None:
            continue

        for cls in r.boxes.cls.tolist():

            name = model.names[int(cls)]

            if name in class_map:
                counts[class_map[name]] += 1
            else:
                counts["OTHER"] += 1

    return counts

# Routes
@app.route("/")
def index():
    return render_template("index.html")


# IMAGE PREDICTION
@app.route("/predict_image", methods=["POST"])
def predict_image():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"})

    # Unique filename (avoids overwrite)
    filename = str(uuid.uuid4()) + ".jpg"
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(upload_path)

    # Run YOLO detection
    results = model(upload_path)
    counts = count_detections(results)

    # Annotated image
    annotated = results[0].plot()
    result_path = os.path.join(RESULT_FOLDER, filename)
    cv2.imwrite(result_path, annotated)

    return jsonify({
        "result_image": "/" + result_path,
        "counts": counts
    })

# ===== Progress Tracker =====
video_progress = {
    "percent": 0
}

# VIDEO PREDICTION
@app.route("/predict_video", methods=["POST"])
def predict_video():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    conf = float(request.form.get("confidence", 0.25))

    filename = str(uuid.uuid4()) + ".mp4"
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(upload_path)

    cap = cv2.VideoCapture(upload_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS) or 25)

    result_path = os.path.join(
        RESULT_FOLDER,
        "annotated_" + filename
    )

    out = cv2.VideoWriter(
        result_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    counts = {
        "D00": 0,
        "D10": 0,
        "D20": 0,
        "D40": 0,
        "OTHER": 0
    }

    # Process frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=conf)
        frame_counts = count_detections(results)

        # Aggregate counts
        for k in counts:
            counts[k] += frame_counts[k]

        annotated = results[0].plot()
        out.write(annotated)

    cap.release()
    out.release()

    return jsonify({
        "result_video": "/" + result_path,
        "counts": counts
    })


# ==========================================
# Run App
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
