import os
import streamlit as st
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="🎷 Smart Music Player", layout="centered")

# === THEME TOGGLE ===
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"

theme_choice = st.sidebar.radio("Select Theme  ☾☼", ["Dark Mode", "Light Mode"],
                                index=0 if st.session_state.theme_mode == "Dark Mode" else 1)

st.session_state.theme_mode = theme_choice

if st.session_state.theme_mode == "Dark Mode":
    text_color = "white"
    bg_color = "#0f0f1a"
    accent_color = "cyan"
else:
    text_color = "black"
    bg_color = "#ffffff"
    accent_color = "blue"

st.markdown(f"<h2 style='color: {text_color}; text-align: center;'>🎵 Music Player </h2>", unsafe_allow_html=True)

st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {bg_color} !important;
    color: {text_color} !important;
}}
section[data-testid="stSidebar"] {{
    background: {bg_color} !important;
    color: {text_color} !important;
}}
div.stButton > button {{
    color: {text_color} !important;
    background-color: {'#0f0f1a' if st.session_state.theme_mode == "Dark Mode" else '#e0e0e0'} !important;
    border: 1px solid {accent_color} !important;
}}
div.streamlit-expanderContent ul li {{
    color: {text_color} !important;
}}
div.streamlit-expanderHeader {{
    color: {text_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# === ALBUM ART IMAGE LOAD ===
base_dir = os.path.dirname(os.path.abspath(__file__))
album_art_path = os.path.join(base_dir, "static", "album_art.png")

if os.path.exists(album_art_path):
    img_data = base64.b64encode(open(album_art_path, "rb").read()).decode()

st.markdown(f"""
<div style="
    width: 220px;
    height: 220px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    border: 6px solid rgba(0,255,255,0.3);
    box-shadow: 0 0 30px rgba(0,255,255,0.6);
    animation: spin 8s linear infinite;">
    <img src="data:image/png;base64,{img_data}" style="
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        display: block;">
</div>

<style>
@keyframes spin {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}
</style>
""", unsafe_allow_html=True)

if "song_index" not in st.session_state:
    st.session_state.song_index = 0
if "last_played_index" not in st.session_state:
    st.session_state.last_played_index = -1
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

songs_dir = os.path.join(base_dir, "songs")

if not os.path.exists(songs_dir):
    st.error(f"❌ Songs folder not found at: {songs_dir}")
    st.stop()

songs = [f for f in os.listdir(songs_dir) if f.endswith(".mp3")]
if not songs:
    st.error("❌ No MP3 files found in /songs folder.")
    st.stop()

current_song = songs[st.session_state.song_index]
audio_file_path = os.path.join(songs_dir, current_song)
audio_bytes = open(audio_file_path, 'rb').read()

st.markdown(f"""
<h4 style='text-align: center; color: {accent_color}; margin-top: 10px; margin-bottom: 8px;'>
🎵 Now Playing: {current_song}
</h4>
""", unsafe_allow_html=True)

st.audio(audio_bytes, format='audio/mp3', start_time=0)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⏮️ Prev"):
        st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
        st.session_state.is_playing = True
        st.rerun()

with col2:
    if st.button("⏭️ Next"):
        st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
        st.session_state.is_playing = True
        st.rerun()

with st.expander("📂 Playlist"):
    st.markdown(f"<ul style='color: {text_color};'>", unsafe_allow_html=True)
    for idx, song in enumerate(songs):
        icon = "🔊 " if idx == st.session_state.song_index else ""
        st.markdown(f"<li>{icon}{song}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div class="about-box" style="color: {text_color};">
        <h2 style="color: {accent_color}; text-align: center;">🎶 About This App</h2>
        <p>
        <strong>SJ Music Player</strong> is a neon-styled, club-vibe music player built with:
        </p>
        <ul>
            <li>🐍 <strong>Python 3</strong></li>
            <li>🎷 <strong>Streamlit</strong></li>
            <li>🖼️ <strong>Base64 Album Art Embedding</strong></li>
        </ul>
        <hr style="border: 1px solid {accent_color};">
        <p>
        <strong>👨‍💻 Created by:</strong> <a href="https://www.linkedin.com/in/samar-abbas-773074278/" target="_blank" style="color: {accent_color};">Samar Abbas</a><br>
        <strong>📍 University of Narowal</strong><br>
        <strong>🧠 Role:</strong> Developer, Designer, and Innovator
        </p>
        <hr style="border: 1px solid {accent_color};">
        <p style="font-style: italic;">💡 Built to feel like Spotify crashed into a Cyberpunk rave club.</p>
    </div>
    """, unsafe_allow_html=True)
