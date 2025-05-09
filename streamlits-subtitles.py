import streamlit as st
from subliminal import download_best_subtitles, save_subtitles, Video
from babelfish import Language
import logging
import tempfile
import os
from pathlib import Path
import shutil

# Configure logging
logging.getLogger('subliminal').setLevel(logging.CRITICAL)

# Page setup
st.set_page_config(page_title="Dev's Subtitle Downloader", layout="centered")

st.title("🎬 Dev's Filename-Based Subtitle Downloader")
st.markdown("""
Upload a `.txt` file containing video filenames (one per line).
The app will fetch English subtitles based on those names using metadata matching.
""")

# File uploader
uploaded_txt = st.file_uploader("📄 Upload your `video_list.txt`", type=["txt"])

# Process uploaded list
if uploaded_txt:
    with tempfile.TemporaryDirectory() as temp_dir:
        lines = uploaded_txt.read().decode("utf-8").splitlines()
        video_names = [line.strip() for line in lines if line.strip()]
        st.info(f"📋 {len(video_names)} file(s) detected in list.")

        for name in video_names:
            st.write(f"🔍 Processing: **{name}**")
            try:
                fake_path = Path(temp_dir) / name
                fake_path.touch()  # Create empty file

                video = Video.fromname(str(fake_path))
                subtitles = download_best_subtitles([video], {Language('eng')}, only_one=True)

                if video in subtitles and subtitles[video]:
                    save_subtitles(video, subtitles[video])
                    subtitle_path = fake_path.with_suffix(".en.srt")
                    final_name = Path(name).with_suffix(".srt")

                    if subtitle_path.exists():
                        with open(subtitle_path, "rb") as srt_file:
                            st.download_button(
                                label=f"⬇️ Download subtitle for: {name}",
                                data=srt_file,
                                file_name=final_name.name,
                                mime="text/plain"
                            )
                            st.success(f"✅ Subtitle ready for: {name}")
                    else:
                        st.warning(f"⚠️ Subtitle saved but not found for: {name}")
                else:
                    st.error(f"❌ No subtitles found for: {name}")
            except Exception as e:
                st.error(f"❌ Error processing {name}: {e}")
else:
    st.info("⬆️ Upload your `video_list.txt` to get started.")
