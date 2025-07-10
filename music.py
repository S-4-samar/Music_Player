import os
import streamlit as st
import pygame
import base64

# Initialize Pygame mixer
# pygame.mixer.init()
audio_file_path = os.path.join(songs_dir, current_song)
audio_bytes = open(audio_file_path, 'rb').read()
st.audio(audio_bytes, format='audio/mp3', start_time=0)

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
songs_dir = os.path.join(base_dir, "songs")
css_file = os.path.join(base_dir, "static", "style.css")
album_art_path = os.path.join(base_dir, "static", "album_art.png")

# === PAGE CONFIG ===
st.set_page_config(page_title="🎧 Smart Music Player", layout="centered")
st.markdown("<h2 style='text-align: center; color: white;'>🚀 Hyper Music Player</h2>", unsafe_allow_html=True)

# === SESSION STATE INIT ===
if "song_index" not in st.session_state:
    st.session_state.song_index = 0
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

# === LOAD SONGS ===
if not os.path.exists(songs_dir):
    st.error(f"❌ Songs folder not found at: {songs_dir}")
    st.stop()

songs = [f for f in os.listdir(songs_dir) if f.endswith(".mp3")]
if not songs:
    st.error("❌ No MP3 files found in /songs folder.")
    st.stop()

# === CSS (responsive tweaks added) ===

responsive_css = """
<style>
body {
    overflow-x: hidden;
}
.visualizer {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    height: 100px;
    margin: 20px 0;
    gap: 5px;
}
.bar {
    width: 6px;
    height: 20px;
    background: cyan;
    animation: bounce 1s infinite ease-in-out;
    border-radius: 10px;
    box-shadow: 0 0 10px cyan;
}
.bar:nth-child(1) { animation-delay: 0s; }
.bar:nth-child(2) { animation-delay: 0.2s; }
.bar:nth-child(3) { animation-delay: 0.4s; }
.bar:nth-child(4) { animation-delay: 0.6s; }
.bar:nth-child(5) { animation-delay: 0.8s; }

@keyframes bounce {
    0%, 100% { height: 20px; }
    50% { height: 80px; }
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(135deg, #111, #1f0036);
    color: white;
    padding: 20px;
    border-right: 2px solid cyan;
    box-shadow: 0 0 20px rgba(0,255,255,0.3);
}

.corner-stripes {
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 100vw;
    pointer-events: none;
    z-index: -1;
}
.stripe {
    position: absolute;
    right: 0;
    height: 4px;
    width: 100%;
    max-width: 400px;
    background: linear-gradient(90deg, cyan, transparent);
    border-radius: 10px;
    animation: moveStripe 3s ease-in-out infinite;
    opacity: 0.5;
}
.stripe:nth-child(1) { top: 10%; animation-delay: 0s; }
.stripe:nth-child(2) { top: 20%; animation-delay: 0.3s; }
.stripe:nth-child(3) { top: 30%; animation-delay: 0.6s; }
.stripe:nth-child(4) { top: 40%; animation-delay: 0.9s; }
.stripe:nth-child(5) { top: 50%; animation-delay: 1.2s; }

@keyframes moveStripe {
    0%, 100% { transform: translateX(0); opacity: 0.2; }
    50% { transform: translateX(-20px); opacity: 0.7; }
}

.blinking .stripe {
    animation: moveStripe 1.2s infinite alternate !important;
    opacity: 0.7 !important;
}

/* Responsive Album Art */
.album-art img {
    width: 90%;
    max-width: 280px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0,255,255,0.3);
    transition: all 0.3s ease-in-out;
}

/* Playlist */
ul {
    padding-left: 20px;
}

/* 🎯 Mobile Tweaks */
@media screen and (max-width: 600px) {
    .visualizer {
        height: 60px;
    }
    .bar {
        width: 4px;
        margin: 0 1px;
    }
    .album-art img {
        width: 100%;
        max-width: 180px;
        margin-top: 10px;
    }
    h4 {
        font-size: 16px !important;
    }
    .element-container button {
        padding: 0.5rem 0.8rem !important;
        font-size: 14px !important;
    }
    .stSlider {
        padding-top: 10px !important;
    }
}
</style>
"""

st.markdown(responsive_css, unsafe_allow_html=True)

# === CORNER STRIPES ===
stripe_class = "corner-stripes blinking" if st.session_state.is_playing else "corner-stripes"
st.markdown(f"""
<div class="{stripe_class}">
    <div class="stripe"></div>
    <div class="stripe"></div>
    <div class="stripe"></div>
    <div class="stripe"></div>
    <div class="stripe"></div>
</div>
""", unsafe_allow_html=True)

# === CURRENT SONG ===
current_song = songs[st.session_state.song_index]

# === ALBUM ART ===
if os.path.exists(album_art_path):
    img_data = base64.b64encode(open(album_art_path, "rb").read()).decode()
    st.markdown(
        f"""
        <div class='album-art' style='text-align: center;'>
            <img src='data:image/png;base64,{img_data}' alt='Album Art'>
        </div>
        """, unsafe_allow_html=True
    )

# === VISUALIZER BARS ===
if st.session_state.is_playing:
    st.markdown("""
    <div class='visualizer'>
        <div class='bar'></div>
        <div class='bar'></div>
        <div class='bar'></div>
        <div class='bar'></div>
        <div class='bar'></div>
    </div>
    """, unsafe_allow_html=True)

# === NOW PLAYING ===
st.markdown(f"<h4 style='color: cyan;'>🎵 Now Playing: {current_song}</h4>", unsafe_allow_html=True)

# === CONTROLS ===
col1, col2, col3 = st.columns(3)

if col1.button("⏮️ Previous", key="prev"):
    st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
    st.session_state.is_playing = False

if col2.button("▶️ Play", key="play"):
    pygame.mixer.music.load(os.path.join(songs_dir, current_song))
    pygame.mixer.music.play()
    st.session_state.is_playing = True

if col3.button("⏹️ Stop", key="stop"):
    pygame.mixer.music.stop()
    st.session_state.is_playing = False

if st.button("⏭️ Next", key="next"):
    st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
    st.session_state.is_playing = False

# === VOLUME SLIDER ===
volume = st.slider("🔊 Volume", 0, 100, 70)
pygame.mixer.music.set_volume(volume / 100)

# === PLAYLIST ===
with st.expander("📂 Playlist"):
    st.markdown("<ul>", unsafe_allow_html=True)
    for idx, song in enumerate(songs):
        icon = "🔊 " if idx == st.session_state.song_index else ""
        st.markdown(f"<li style='color: white;'>{icon}{song}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)

# === SIDEBAR INFO ===
with st.sidebar:
    st.markdown("## 🎶 About This App")
    st.markdown("""
    **Hyper Music Player** is a neon-styled, club-vibe music player built with:

    - 🐍 **Python 3**
    - 🎧 **Pygame**
    - 🌐 **Streamlit**
    - 🖼️ **Base64 Album Art Embedding**
    
    ---
    **👨‍💻 Created by:** [Samar Abbas](https://www.linkedin.com/in/samar-abbas-773074278/)  
    **📍 University of Narowal**  
    **🧠 Role:** Developer, Designer, and Innovator  
    """)
    st.markdown("---")
    st.markdown("💡 *Built to feel like Spotify crashed into a Cyberpunk rave club.*")
