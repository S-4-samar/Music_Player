import os
import streamlit as st
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="🎷 Smart Music Player", layout="centered")

# === SESSION STATE INIT ===
if "song_index" not in st.session_state:
    st.session_state.song_index = 0
if "last_played_index" not in st.session_state:
    st.session_state.last_played_index = -1
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

# === Paths ===
base_dir = os.path.dirname(os.path.abspath(__file__))
songs_dir = os.path.join(base_dir, "songs")
album_art_path = os.path.join(base_dir, "static", "album_art.png")

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

# === ALBUM ART ===
img_data = base64.b64encode(open(album_art_path, "rb").read()).decode()

# === PAGE TITLE ===
st.markdown("<h2 style='text-align: center; color: white;'>🎵 Music Player</h2>", unsafe_allow_html=True)

# === CONDITIONAL ROTATION STYLE ===
if st.session_state.is_playing:
    rotation_style = """
    <style>
    .album-spin {
        animation: spin 8s linear infinite;
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    </style>
    """
else:
    rotation_style = "<style>.album-spin { animation: none; }</style>"

st.markdown(rotation_style, unsafe_allow_html=True)

st.markdown(f"""
<div style="
    width: 220px;
    height: 220px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    border: 6px solid rgba(0,255,255,0.3);
    box-shadow: 0 0 30px rgba(0,255,255,0.6);
" class="album-spin">
    <img src="data:image/png;base64,{img_data}" style="
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        display: block;
    ">
</div>
""", unsafe_allow_html=True)

# === AUDIO PLAYER ===
st.audio(audio_bytes, format='audio/mp3', start_time=0)

# === CONTROLS ===
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⏮️ Prev"):
        st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
        st.session_state.is_playing = True
        st.rerun()

with col2:
    if st.button("▶️ Play"):
        st.session_state.is_playing = True
        st.rerun()

with col3:
    if st.button("⏹️ Stop"):
        st.session_state.is_playing = False
        st.rerun()

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
    - 🎷 **Streamlit**
    - 🖼️ **Base64 Album Art Embedding**

    ---
    **👨‍💻 Created by:** [Samar Abbas](https://www.linkedin.com/in/samar-abbas-773074278/)  
    **📍 University of Narowal**  
    **🧠 Role:** Developer, Designer, and Innovator  
    """)
    st.markdown("---")
    st.markdown("💡 *Built to feel like Spotify crashed into a Cyberpunk rave club.*")
