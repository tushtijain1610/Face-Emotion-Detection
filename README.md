Facial Emotion Detection 🧠
This project is a real-time facial emotion detection web app built with Streamlit. It allows users to upload an image or use their webcam to detect and visualize emotions like happiness, sadness, anger, surprise, fear, disgust, and neutral expressions.

✨ Features
📸 Upload Image → Analyze emotions from a static photo

🎥 Use Webcam → Perform real-time emotion detection on live video

📊 Visual Reports → See emotion confidence scores in bar charts

🎨 Interactive UI → Color-coded results with emoji and descriptions

🏗️ Adjustable settings for detection backend, model type, and confidence thresholds

🛠 Technologies Used
Python

Streamlit (web app framework)

OpenCV (face detection)

Pandas & Altair (data display & visualization)

NumPy, Pillow, streamlit-lottie

🚀 How to Run
1️⃣ Clone the repository:
git clone https://github.com/yourusername/face_emotion_detection.git
cd face_emotion_detection

2️⃣ Install dependencies:
pip install -r requirements.txt

3️⃣ Run the Streamlit app:
streamlit run app.py

4️⃣ Open your browser and navigate to:
http://localhost:8501

📂 Project Structure
/face_emotion_detection
  └── app.py
  └── requirements.txt
  └── README.md
  └── [additional files if any]
  
💡 Notes
The emotion predictions are simulated/random in this version. You can integrate a real trained model (like fer, deepface, etc.) for actual predictions.

Make sure your webcam has permissions enabled if using the webcam mode.

👥 Authors
AI Emotion Analysis Team

Version 2.0
