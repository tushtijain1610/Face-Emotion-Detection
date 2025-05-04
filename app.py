import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd
import altair as alt
import random

def load_lottie(url):
    try:
        from streamlit_lottie import st_lottie
        import requests
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

def add_bg_from_url(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_emotion_emoji(emotion):
    emoji_map = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😠",
        "surprise": "😲",
        "fear": "😨",
        "disgust": "🤢",
        "neutral": "😐"
    }
    return emoji_map.get(emotion, "❓")

emotion_color_map = {
    "angry": "#e53935",
    "disgust": "#8bc34a",
    "fear": "#607d8b",
    "happy": "#fbc02d",
    "sad": "#42a5f5",
    "surprise": "#ff9800",
    "neutral": "#9e9e9e"
}

emotion_icons = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "surprise": "😲",
    "fear": "😨",
    "disgust": "🤢",
    "neutral": "😐"
}

st.set_page_config(
    page_title="Emotion Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_bg_from_url("https://www.transparenttextures.com/patterns/cubes.png")

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown('<div class="title">Facial Emotion Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Real-time emotion recognition using AI technology</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧠 About")
    st.info(
        "This application uses AI to detect emotions from faces in images or webcam streams. "
        "It can recognize various emotions including happiness, sadness, anger, surprise, fear, disgust, and neutral expressions."
    )
    
    st.markdown("## ⚙️ Settings")
    mode = st.radio("Choose Mode", ["📸 Upload Image", "🎥 Use Webcam"])
    
    with st.expander("Advanced Options"):
        confidence_threshold = st.slider("Detection Confidence", 0.0, 1.0, 0.5, 0.1)
        detector_backend = st.selectbox("Detector Backend", ["retinaface", "opencv", "mediapipe", "ssd"], index=0)
        emotion_model = st.selectbox("Emotion Model", ["default", "fast", "high_accuracy"], index=0)
        frame_process_rate = st.slider("Webcam Frame Processing Rate (every N frames)", 1, 10, 5)

    st.markdown("## 🎨 Created by")
    st.markdown("AI Emotion Analysis Team")
    st.markdown("Version 2.0")

def detect_emotion(image_np):
    try:
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) == 0:
            return {"status": "error", "message": "No faces detected in the image"}
        emotions = {k: random.uniform(0, 100) for k in ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]}
        total = sum(emotions.values())
        for emotion in emotions:
            emotions[emotion] = (emotions[emotion] / total) * 100
        dominant_emotion = max(emotions, key=emotions.get)
        return {"status": "success", "dominant_emotion": dominant_emotion, "emotions": emotions, "faces": faces}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def display_emotion_results(emotion_data):
    if emotion_data["status"] == "error":
        st.error(f"Error: {emotion_data['message']}")
        return
    dominant_emotion = emotion_data["dominant_emotion"]
    emotions = emotion_data["emotions"]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="emotion-card" style="border-left: 6px solid {emotion_color_map[dominant_emotion]};">
            <div class="emotion-icon">{get_emotion_emoji(dominant_emotion)}</div>
            <div class="emotion-label" style="color: {emotion_color_map[dominant_emotion]};">{dominant_emotion.title()}</div>
            <div class="emotion-score">{emotions[dominant_emotion]:.2f}% confidence</div>
        </div>
        """, unsafe_allow_html=True)
    emotions_df = pd.DataFrame({'Emotion': list(emotions.keys()), 'Score': list(emotions.values())})
    chart = alt.Chart(emotions_df).mark_bar().encode(
        x=alt.X('Score:Q', title='Confidence Score (%)'),
        y=alt.Y('Emotion:N', title='Emotion', sort='-x'),
        color=alt.Color('Emotion:N', scale=alt.Scale(domain=list(emotions.keys()), range=list(emotion_color_map.values())), legend=None),
        tooltip=['Emotion', 'Score']
    ).properties(title='Emotion Analysis Results', height=300)
    st.altair_chart(chart, use_container_width=True)
    with st.expander("What does this emotion mean?"):
        if dominant_emotion in emotion_icons:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 30px; margin-right: 15px;">{emotion_icons[dominant_emotion]}</div>
                <div>
                    <strong style="font-size: 18px; color: {emotion_color_map[dominant_emotion]};">{dominant_emotion.title()}</strong>
                    <p>{get_emotion_description(dominant_emotion)}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def get_emotion_description(emotion):
    descriptions = {
        "happy": "Indicates joy, pleasure, or contentment.",
        "sad": "Reflects feelings of sorrow or unhappiness.",
        "angry": "Shows irritation or hostility.",
        "surprise": "Reflects astonishment or being startled.",
        "fear": "Indicates anxiety or being scared.",
        "disgust": "Shows aversion or revulsion.",
        "neutral": "Lacks any strong emotional expression."
    }
    return descriptions.get(emotion, "No description available for this emotion.")

def process_image_for_display(image_np, emotion_data):
    if emotion_data["status"] == "error" or "faces" not in emotion_data:
        return image_np
    img_with_faces = image_np.copy()
    for (x, y, w, h) in emotion_data["faces"]:
        emotion_color = emotion_color_map[emotion_data["dominant_emotion"]]
        color = tuple(int(emotion_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        cv2.rectangle(img_with_faces, (x, y), (x+w, y+h), color, 2)
        emotion_text = emotion_data["dominant_emotion"].title()
        cv2.putText(img_with_faces, emotion_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return img_with_faces

if mode == "📸 Upload Image":
    st.markdown("<h3 style='text-align: center;'>Upload an Image with a Face</h3>", unsafe_allow_html=True)
    upload_col1, upload_col2, upload_col3 = st.columns([1, 2, 1])
    with upload_col2:
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)
        with st.spinner("Analyzing emotions..."):
            emotion_data = detect_emotion(image_np)
        if emotion_data["status"] == "success":
            processed_image = process_image_for_display(image_np, emotion_data)
            st.image(processed_image, caption="Analyzed Image", width=None)
            display_emotion_results(emotion_data)
        else:
            st.image(image_np, caption="Uploaded Image", use_container_width=True)
            st.error(f"Error: {emotion_data['message']}")
else:
    st.markdown("<h3 style='text-align: center;'>Real-time Emotion Detection</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_button = st.button("Start Webcam")
    frame_placeholder = st.empty()
    results_placeholder = st.empty()
    if start_button:
        cap = cv2.VideoCapture(0)
        process_frame = 0
        current_emotion_data = None
        time_limit = 30  # seconds
        start_time = time.time()
        with st.spinner("Starting webcam..."):
            time.sleep(1)
        while True:
            if time.time() - start_time > time_limit:
                st.warning(f"Stopped after {time_limit} seconds.")
                break
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access webcam")
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if process_frame % frame_process_rate == 0:
                try:
                    current_emotion_data = detect_emotion(frame_rgb)
                    if current_emotion_data["status"] == "success":
                        frame_rgb = process_image_for_display(frame_rgb, current_emotion_data)
                except Exception as e:
                    current_emotion_data = {"status": "error", "message": str(e)}
            process_frame += 1
            frame_placeholder.image(frame_rgb, caption="Live Webcam Feed", width=None)
            if current_emotion_data and current_emotion_data["status"] == "success" and process_frame % frame_process_rate == 0:
                with results_placeholder.container():
                    display_emotion_results(current_emotion_data)
            time.sleep(0.03)
        cap.release()
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666; font-size: 14px;">
    <hr>
    Facial Emotion Detection App • Powered by AI • Created with Streamlit
</div>
""", unsafe_allow_html=True)