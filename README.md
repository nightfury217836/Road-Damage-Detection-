# How I Built a 🚧 Road Pothole Detection System 🔥 | Computer Vision + Machine Learning Project

<img width="1918" height="1078" alt="Screenshot 2026-02-17 144744" src="https://github.com/user-attachments/assets/33333dfa-a767-4258-a449-455e3d47bf38" />

💡 Ever wondered if Artificial Intelligence can detect dangerous potholes and other road damages before accidents happen?

In this video, I’ll show you how I built a Road Damage Detection System using YOLOv11 Object Detection and Machine Learning — a complete real-time Computer Vision project. 🚧🤖

<img width="1280" height="720" alt="SQL_Thumbnail (75)" src="https://github.com/user-attachments/assets/308a4678-217f-40f0-b5fe-d3aa277a2517" />

🔗 Youtube Link: https://youtu.be/vPvTgB9Xt3Q?si=HugQqEbrswArot1k

---

## 🚧 Introduction & Problem

0:00 Introduction to Road Damage Problem  
0:10 Project Demo  
1:18 Introducing Marg Rakshak – AI Road Damage Detection System  

---

## 🤖 System Overview

2:19 System Capabilities and Benefits  
3:16 Future Development & Version 2.0 Plans  

---

## 📁 Project Setup & Dataset

4:13 Project Setup and Folder Structure  
4:52 Downloading the RDD 2022 Road Damage Dataset  

---

## 💻 Flask Web Application (app.py)

5:49 app.py Overview  
5:52 Importing Required Libraries  
7:01 Flask App Configuration & Server Initialization  
7:34 Loading the Trained YOLO Model  
8:14 Counting Detected Road Defects  
12:25 Homepage Route Explanation  
12:52 Image Prediction Pipeline  

---

## 🎥 Video Detection Pipeline

18:33 Video Prediction Route Overview  
18:38 Video Upload Validation  
18:51 Video Reader & Writer Initialization  
19:23 Defect Counter Initialization  
19:32 Frame-by-Frame Detection Loop  
27:19 Releasing Resources & Returning Results  
27:39 Running the Flask Application  

---

## 🔄 Converting XML Dataset to YOLO Format

27:59 Why XML Must Be Converted to YOLO Format  
28:37 Importing Conversion Libraries  
29:54 Class Mapping for Road Damage Types  
30:47 Input & Output Directory Setup  
31:11 Converting Bounding Boxes to YOLO Format  
32:24 Converting Training Data  
35:52 Processing XML Files & Extracting Image Dimensions  
42:56 Creating YOLO Label Files & Copying Images  
46:06 Preparing Test Images  
46:14 Main Execution Script  

---

## 🧠 Model Training (train.py)

46:38 Training Script Overview  
46:41 Importing Training Libraries  
47:05 Device Definition & CUDA Check  
47:39 Loading Pre-trained YOLO Model  
48:17 Training Parameters Explained  
50:58 Training Setup Summary  

---

We’ll go step by step:  
✅ Understanding the Road Damage Dataset  
✅ Converting XML annotations to YOLO format  
✅ Training a custom YOLO model on CPU  
✅ Detecting potholes and cracks in images & videos  
✅ Generating annotated outputs with bounding boxes  
✅ Deploying the model into a working application  

This is a full **End-to-End YOLO Object Detection Project** — perfect for students, beginners, and anyone building a strong AI/ML portfolio.

---

✨ By the end, you’ll learn how to:  
• Prepare and structure a custom dataset  
• Train a YOLO model using transfer learning  
• Tune confidence threshold and optimize performance  
• Detect road defects in real-world scenarios  
• Build a deployable ML application  

---

📌 **Technologies Used:** Python, YOLO (Ultralytics), OpenCV, PyTorch, Machine Learning  

💬 If you’re starting in AI/ML or Computer Vision, this tutorial shows how to turn a real-world problem into a production-ready solution.

🔔 Subscribe for more AI, ML, and Python projects: @SouvikChai

📢 Share this project with friends who love Computer Vision & AI!
