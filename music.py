import os
import streamlit as st
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="🎷 Smart Music Player", layout="centered")
st.markdown("<h2 style='text-align: center; color: white;'>🚀 Hyper Music Player</h2>", unsafe_allow_html=True)

# === SESSION STATE INIT (important to avoid AttributeError) ===
if "song_index" not in st.session_state:
    st.session_state.song_index = 0
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

# === CSS ===
responsive_css = """
<style>
body {
    overflow-x: hidden;
}
.album-art img {
    width: 90%;
    max-width: 280px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0,255,255,0.3);
    transition: all 0.3s ease-in-out;
}
ul {
    padding-left: 20px;
}
@media screen and (max-width: 600px) {
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
}
</style>
"""
st.markdown(responsive_css, unsafe_allow_html=True)

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
st.markdown(f"""
<h4 style='text-align: center; color: cyan; margin-top: 10px; margin-bottom: 8px;'>
🎵 Now Playing: {current_song}
</h4>
""", unsafe_allow_html=True)


# === STREAMLIT AUDIO PLAYER ===
st.audio(audio_bytes, format='audio/mp3', start_time=0)

# === CONTROLS (Previous & Next on same line) ===
# === CONTROLS (Previous & Next on same line) ===
col1, spacer, col2 = st.columns([1, 5, 1])
with col1:
    if st.button("⏭️ Next", key="next"):
        st.session_state.song_index = (st.session_state.song_index + 1) % len(songs)
        st.session_state.is_playing = False

with col2:
    if st.button("⏮️ Prev", key="prev"):
        st.session_state.song_index = (st.session_state.song_index - 1) % len(songs)
        st.session_state.is_playing = False
        
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
