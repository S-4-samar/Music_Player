import os
import streamlit as st
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="🎷 Smart Music Player", layout="centered")
st.markdown("<h2 style='text-align: center; color: white;'>🎵 Music Player</h2>", unsafe_allow_html=True)

# === ALBUM ART IMAGE LOAD FIRST TO USE IN F-STRING ===
base_dir = os.path.dirname(os.path.abspath(__file__))
album_art_path = os.path.join(base_dir, "static", "album_art.png")

if os.path.exists(album_art_path):
    img_data = base64.b64encode(open(album_art_path, "rb").read()).decode()

# === ROTATING ALBUM ART ===
st.markdown(f"""
<div style="
    width: 180px;
    height: 180px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid rgba(0,255,255,0.3);
    box-shadow: 0 0 20px rgba(0,255,255,0.6);
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

# === SESSION STATE INIT ===
if "song_index" not in st.session_state:
    st.session_state.song_index = 0
if "last_played_index" not in st.session_state:
    st.session_state.last_played_index = -1
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

# === Paths ===
songs_dir = os.path.join(base_dir, "songs")

# === LOAD SONGS ===
if not os.path.exists(songs_dir):
    st.error(f"❌ Songs folder not found at: {songs_dir}")
    st.stop()

songs = [f for f in os.listdir(songs_dir) if f.endswith(".mp3")]
if not songs:
    st.error("❌ No MP3 files found in /songs folder.")
    st.stop()

# === CURRENT SONG ===
current_song = songs[st.session_state.song_index]
audio_file_path = os.path.join(songs_dir, current_song)
audio_bytes = open(audio_file_path, 'rb').read()

# === CSS ===
st.markdown("""
<style>
body {
    overflow-x: hidden;
    margin: 0;
}
.album-art img {
    width: 90%;
    max-width: 200px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0,255,255,0.3);
    transition: all 0.3s ease-in-out;
}
.visualizer {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    height: 60px;
    margin-top: 10px;
    gap: 3px;
}
.bar {
    width: 5px;
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
    50% { height: 40px; }
}
ul {
    padding-left: 16px;
}
@media screen and (max-width: 600px) {
    .album-art img {
        width: 80%;
        max-width: 150px;
        margin-top: 5px;
    }
    h4 {
        font-size: 14px !important;
    }
    .element-container button {
        padding: 0.4rem 0.7rem !important;
        font-size: 12px !important;
    }
    .visualizer {
        height: 50px;
        gap: 2px;
    }
}
</style>
""", unsafe_allow_html=True)

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
    for i in range(60)
]) + "</div>", unsafe_allow_html=True)

# === NOW PLAYING ===
st.markdown(f"""
<h4 style='text-align: center; color: cyan; margin-top: 10px; margin-bottom: 8px;'>
🎵 Now Playing: {current_song}
</h4>
""", unsafe_allow_html=True)

# === STREAMLIT AUDIO PLAYER ===
st.audio(audio_bytes, format='audio/mp3', start_time=0)

# === CONTROLS ===
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

# === PLAYLIST ===
with st.expander("📂 Playlist"):
    st.markdown("<ul>", unsafe_allow_html=True)
    for idx, song in enumerate(songs):
        icon = "🔊 " if idx == st.session_state.song_index else ""
        st.markdown(f"<li style='color: white;'>{icon}{song}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        border: 3px solid red;
        border-radius: 15px;
        box-shadow:
            0 0 15px red,
            0 0 30px red,
            0 0 45px red;
        padding: 10px;
        max-height: 100vh;
        overflow: hidden;
    }
    .about-box {
        padding: 15px;
        border: 2px solid cyan;
        border-radius: 10px;
        background: rgba(0, 0, 0, 0.5);
        box-shadow:
            0 0 15px cyan,
            0 0 30px cyan,
            0 0 45px cyan,
            inset 0 0 8px rgba(0,255,255,0.3);
        transition: all 0.3s ease-in-out;
    }
    .about-box:hover {
        box-shadow:
            0 0 20px cyan,
            0 0 40px cyan,
            0 0 60px cyan,
            inset 0 0 15px rgba(0,255,255,0.4);
    }
    </style>

    <div class="about-box">
        <h2 style="color: cyan; text-align: center; font-size: 18px;">🎶 About This App</h2>
        <p style="font-size: 13px;">
        <strong>SJ Music Player</strong> is a neon-styled, club-vibe music player built with:
        </p>
        <ul style="font-size: 13px;">
            <li>🐍 <strong>Python 3</strong></li>
            <li>🎷 <strong>Streamlit</strong></li>
            <li>🖼️ <strong>Base64 Album Art Embedding</strong></li>
        </ul>
        <hr style="border: 1px solid cyan;">
        <p style="font-size: 13px;">
        <strong>👨‍💻 Created by:</strong> <a href="https://www.linkedin.com/in/samar-abbas-773074278/" target="_blank" style="color: cyan;">Samar Abbas</a><br>
        <strong>📍 University of Narowal</strong><br>
        <strong>🧠 Role:</strong> Developer, Designer, and Innovator
        </p>
        <hr style="border: 1px solid cyan;">
        <p style="font-style: italic; font-size: 12px;">💡 Built to feel like Spotify crashed into a Cyberpunk rave club.</p>
    </div>
    """, unsafe_allow_html=True)
