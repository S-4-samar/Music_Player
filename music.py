import os
import streamlit as st
import streamlit.components.v1 as components
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="🎷 Smart Music Player", layout="centered")

# === SESSION STATE INIT ===
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"
if "song_index" not in st.session_state:
    st.session_state.song_index = 0
if "last_played_index" not in st.session_state:
    st.session_state.last_played_index = -1
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
if "processed" not in st.session_state:
    st.session_state.processed = False

# === THEME CHOICE ===
theme_choice = st.sidebar.radio("**Select Theme  ☾☼**", ["Dark Mode", "Light Mode"],
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

st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {bg_color} !important;
    color: {text_color} !important;
}}
section[data-testid="stSidebar"] {{
    background: {bg_color} !important;
    color: {text_color} !important;
    border: 3px solid red;
    border-radius: 20px;
    box-shadow: 0 0 20px red, 0 0 40px red, 0 0 60px red;
    padding: 10px;
}}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div[role="radiogroup"] label div,
section[data-testid="stSidebar"] div[role="radiogroup"] label span {{
    color: {text_color} !important;
    font-weight: 600;
}}

/* Buttons and Playlist Items */
div.stButton > button {{
    color: {text_color} !important;
    background-color: {'#0f0f1a' if st.session_state.theme_mode == "Dark Mode" else '#e0e0e0'} !important;
    border: 1px solid {accent_color} !important;
}}
div.streamlit-expanderContent ul li,
div.streamlit-expanderHeader {{
    color: {text_color} !important;
}}

/* Sidebar content fit */
section[data-testid="stSidebar"] {{
    max-height: 100vh;
    overflow: hidden;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h2 style='color: {text_color}; text-align: center;'>🎵 Music Player</h2>", unsafe_allow_html=True)

# === ALBUM ART ===
base_dir = os.path.dirname(os.path.abspath(__file__))
album_art_path = os.path.join(base_dir, "static", "album_art.png")
if os.path.exists(album_art_path):
    img_data = base64.b64encode(open(album_art_path, "rb").read()).decode()

st.markdown(f"""
<div style="width: 220px; height: 220px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 6px solid rgba(0,255,255,0.3); box-shadow: 0 0 30px rgba(0,255,255,0.6); animation: spin 8s linear infinite;">
    <img src="data:image/png;base64,{img_data}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block;">
</div>
<style>
@keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# === SONGS ===
songs_dir = os.path.join(base_dir, "songs")
songs = [f for f in os.listdir(songs_dir) if f.endswith(".mp3")]
current_song = songs[st.session_state.song_index]
audio_file_path = os.path.join(songs_dir, current_song)
audio_bytes = open(audio_file_path, 'rb').read()

# === VOICE CONTROL ===
st.markdown("## 🎙️ Voice Control (Browser-based)")
components.html(f"""
    <button onclick="startListening()" style="padding: 10px; font-size: 18px; border-radius: 8px;">🎙️ Start Voice Command</button>
    <p id="result" style="font-weight: bold; font-size: 20px;"></p>
    <script>
    function startListening() {{
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event) {{
            var command = event.results[0][0].transcript;
            document.getElementById('result').innerText = 'You said: ' + command;
            window.location.search = '?command=' + encodeURIComponent(command);
        }};
    }}
    </script>
""", height=200)

# === HANDLE COMMAND ===
command = st.query_params.get("command", [None])[0]
if command and not st.session_state.processed:
    st.session_state.processed = True
    command = command.lower()
    if "next" in command:
        st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
        st.rerun()
    elif "previous" in command or "prev" in command:
        st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
        st.rerun()
    elif "play" in command:
        st.session_state.is_playing = True
        st.rerun()
    elif "stop" in command or "pause" in command:
        st.session_state.is_playing = False
        st.rerun()

# === NOW PLAYING ===
st.markdown(f"""<h4 style='text-align: center; color: cyan; margin-top: 10px; margin-bottom: 8px;'>🎵 Now Playing: {current_song}</h4>""", unsafe_allow_html=True)
st.audio(audio_bytes, format='audio/mp3', start_time=0)

# === CONTROLS ===
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⏭️ Next"):
        st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
        st.session_state.is_playing = True
        st.rerun()
with col2:
    if st.button("⏮️ Prev"):
        st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
        st.session_state.is_playing = True
        st.rerun()

# === PLAYLIST ===
with st.expander("📂 Playlist"):
    st.markdown(f"<ul style='color: {text_color};'>", unsafe_allow_html=True)
    for idx, song in enumerate(songs):
        icon = "🔊 " if idx == st.session_state.song_index else ""
        st.markdown(f"<li>{icon}{song}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)

# === NEON STARS ===
st.markdown("""
<style>
.neon-stars-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
}

.neon-stars-overlay .star {
    position: absolute;
    width: 2px;
    height: 2px;
    border-radius: 50%;
    background: cyan;
    box-shadow: 0 0 8px cyan;
    animation: neon-blink 3s infinite ease-in-out;
}

@keyframes neon-blink {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.4); }
}
</style>

<div class="neon-stars-overlay">
""" + 
"\n".join([
    f'<div class="star" style="top:{i * 2 % 100}vh; left:{(i * i * 3) % 100}vw; animation-delay:{(i % 10) * 0.2}s;"></div>'
    for i in range(100)
]) + 
"</div>", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.markdown(f"""
    <div class="about-box">
        <h2 style="color: cyan; text-align: center;">🎶 About This App</h2>
        <p><strong>SJ Music Player</strong> is a neon-styled, club-vibe music player built with:</p>
        <ul>
            <li>🐍 <strong>Python 3</strong></li>
            <li>🎷 <strong>Streamlit</strong></li>
            <li>🖼️ <strong>Base64 Album Art Embedding</strong></li>
        </ul>
        <hr style="border: 1px solid cyan;">
        <p><strong>👨‍💻 Created by:</strong> <a href="https://www.linkedin.com/in/samar-abbas-95a235287" target="_blank" style="color: cyan;">Samar Abbas</a><br>
        <strong>📍 University of Narowal</strong><br>
        <strong>👨🏽‍💻 Role:</strong> Developer, Designer, and Innovator</p>
        <hr style="border: 1px solid cyan;">
        <p style="font-style: italic;">💡 Built to feel like Spotify crashed into a Cyberpunk rave club.</p>
    </div>
    <style>
    .about-box {{ padding: 20px; border: 2px solid cyan; border-radius: 15px; background: rgba(0, 0, 0, 0.5); box-shadow: 0 0 20px cyan, 0 0 40px cyan, 0 0 60px cyan, inset 0 0 10px rgba(0,255,255,0.3); transition: all 0.3s ease-in-out; }}
    .about-box:hover {{ box-shadow: 0 0 30px cyan, 0 0 60px cyan, 0 0 90px cyan, inset 0 0 20px rgba(0,255,255,0.4); }}
    </style>
    """, unsafe_allow_html=True)
