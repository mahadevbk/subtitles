import os
from tkinter import Tk, filedialog, messagebox
from subliminal import download_best_subtitles, save_subtitles, Video
from babelfish import Language
import logging

# Suppress subliminal log noise
logging.getLogger('subliminal').setLevel(logging.CRITICAL)

# Select multiple video files via GUI
def pick_video_files():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select one or more video files",
        filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov *.flv *.wmv *.webm")]
    )
    return list(file_paths)

# Download subtitles and rename them to match the video filename
def download_subtitles():
    video_paths = pick_video_files()

    if not video_paths:
        print("❌ No files selected.")
        return

    print(f"🎬 Selected {len(video_paths)} file(s):")
    for path in video_paths:
        print(f"   - {path}")

    for path in video_paths:
        if not os.path.isfile(path):
            print(f"⚠️ Skipping invalid file: {path}")
            continue

        try:
            video = Video.fromname(path)
            subtitles = download_best_subtitles([video], {Language('eng')}, only_one=True)

            if video in subtitles and subtitles[video]:
                save_subtitles(video, subtitles[video])
                print(f"✅ Subtitle downloaded for: {os.path.basename(path)}")

                # Rename downloaded subtitle from .en.srt to .srt
                base, _ = os.path.splitext(path)
                default_sub = base + ".en.srt"
                final_sub = base + ".srt"

                if os.path.exists(default_sub):
                    os.rename(default_sub, final_sub)
                    print(f"📁 Renamed subtitle to: {os.path.basename(final_sub)}")
                else:
                    print(f"⚠️ Expected subtitle not found: {default_sub}")
            else:
                print(f"❌ No subtitles found for: {os.path.basename(path)}")
        except Exception as e:
            print(f"❌ Error processing '{path}': {e}")

    messagebox.showinfo("Done", "Subtitle download process completed.")

if __name__ == "__main__":
    download_subtitles()

