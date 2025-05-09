import os
import tempfile
import streamlit as st
from subliminal import download_best_subtitles, save_subtitles, Video
from babelfish import Language
import logging
from pathlib import Path

# Suppress subliminal log output
logging.getLogger('subliminal').setLevel(logging.CRITICAL)

st.set_page_config(page_title="Dev's Subtitle Downloader", layout="centered")

st.title("🎬 Dev's Subtitle Downloader")
st.markdown("Upload one or more video files and the app will fetch and rename the best-matching **English** subtitles.")

# File uploader
uploaded_files = st.file_uploader("📂 Upload video files", type=["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"🔍 Processing {len(uploaded_files)} file(s)...")

    for uploaded_file in uploaded_files:
        # Write uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_video:
            temp_video.write(uploaded_file.read())
            temp_video_path = temp_video.name

        st.write(f"📄 **{uploaded_file.name}**")

        try:
            video = Video.fromname(temp_video_path)
            subtitles = download_best_subtitles([video], {Language('eng')}, only_one=True)

            if video in subtitles and subtitles[video]:
                save_subtitles(video, subtitles[video])

                subtitle_path = Path(temp_video_path).with_suffix(".en.srt")
                final_subtitle_name = Path(uploaded_file.name).with_suffix(".srt")

                if subtitle_path.exists():
                    with open(subtitle_path, "rb") as sub_file:
                        st.download_button(
                            label=f"⬇️ Download subtitle for {uploaded_file.name}",
                            data=sub_file,
                            file_name=str(final_subtitle_name),
                            mime="text/plain"
                        )
                        st.success("✅ Subtitle ready!")
                    os.remove(subtitle_path)
                else:
                    st.warning("⚠️ Subtitle downloaded but could not be found or renamed.")
            else:
                st.error("❌ No matching subtitles found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

        os.remove(temp_video_path)

else:
    st.info("⬆️ Upload one or more video files to get started.")

