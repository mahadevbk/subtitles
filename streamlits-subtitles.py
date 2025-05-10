import streamlit as st
from subliminal import download_best_subtitles, save_subtitles, Video
from babelfish import Language
import logging
import tempfile
from pathlib import Path

# Configure logging
logging.getLogger('subliminal').setLevel(logging.CRITICAL)

# Page setup
st.set_page_config(page_title="Dev's Subtitle Downloader", layout="centered")
st.title("🎬 Dev's Filename-Based Subtitle Downloader")

st.markdown("""
Paste up to 5 video filenames below (one per input box).
The app will fetch English subtitles based on those names using matching metadata.  
There is also a pure python script in the github folder using tkinter that is more effective but needs to run on your local machine. 

Streamlit tries to upload all the files before it can process the complete metadata ; with a file upload limit of 200mb, this is unfeasible. Therefore, the streamlit version is limited to pasting file names to fetch data.
""")

# Input for up to 10 filenames
video_names = []
for i in range(5):
    filename = st.text_input(f"Video filename {i+1}")
    if filename.strip():
        video_names.append(filename.strip())

if video_names:
    st.info(f"📋 {len(video_names)} file(s) entered.")

    with tempfile.TemporaryDirectory() as temp_dir:
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
    st.info("✏️ Enter at least one filename above to begin.")
