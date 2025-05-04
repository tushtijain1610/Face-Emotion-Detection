import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie

# Function to add background image
def add_bg_from_url(url):
    """
    Add a background image to Streamlit app from a URL
    """
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

# Function to load Lottie animations
def load_lottie(url: str):
    """
    Load Lottie animation from URL
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        print(f"Error loading Lottie animation: {e}")
        return None

# Emotion color mapping
emotion_color_map = {
    "angry": "#E53935",    # Red
    "disgust": "#8BC34A",  # Green
    "fear": "#7E57C2",     # Purple
    "happy": "#FFB300",    # Amber
    "sad": "#42A5F5",      # Blue
    "surprise": "#FF7043", # Deep Orange
    "neutral": "#78909C"   # Blue Grey
}

# Get emoji for each emotion
def get_emotion_emoji(emotion):
    """
    Return emoji for a given emotion
    """
    emoji_map = {
        "angry": "😠",
        "disgust": "🤢",
        "fear": "😨",
        "happy": "😊",
        "sad": "😔",
        "surprise": "😲",
        "neutral": "😐"
    }
    return emoji_map.get(emotion, "❓")