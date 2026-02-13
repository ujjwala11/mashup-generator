
import sys
import os
import shutil
import yt_dlp
from pydub import AudioSegment
from tqdm import tqdm

# Folder structure
DOWNLOAD_FOLDER = "downloads"
MP3_FOLDER = "mp3"
CUT_FOLDER = "cut"


# ---------------------------
# Create folders safely
# ---------------------------
def setup_folders():

    folders = [DOWNLOAD_FOLDER, MP3_FOLDER, CUT_FOLDER]

    for folder in folders:

        if not os.path.exists(folder):
            os.makedirs(folder)

        else:
            # Delete only files inside (NOT folder itself)
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except:
                    pass


# ---------------------------
# Download videos
# ---------------------------
def download_videos(singer, num_videos):

    print(f"\nSearching and downloading {num_videos} videos of {singer}...\n")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    search_query = f"ytsearch{num_videos}:{singer}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=True)

    files = []

    for entry in info['entries']:
        ext = entry.get('ext', 'webm')
        title = entry['title'].replace("/", "").replace("\\", "")
        files.append(f"{DOWNLOAD_FOLDER}/{title}.{ext}")

    print("Download completed.\n")
    return files


# ---------------------------
# Convert to mp3
# ---------------------------
def convert_to_mp3(video_files):

    print("Converting videos to mp3...\n")

    mp3_files = []

    for file in tqdm(video_files):

        try:
            audio = AudioSegment.from_file(file)

            filename = os.path.basename(file).split('.')[0]
            mp3_path = f"{MP3_FOLDER}/{filename}.mp3"

            audio.export(mp3_path, format="mp3")

            mp3_files.append(mp3_path)

        except Exception as e:
            print("Conversion failed:", file)

    print("Conversion completed.\n")
    return mp3_files


# ---------------------------
# Cut audio
# ---------------------------
def cut_audio(mp3_files, duration):

    print(f"Cutting first {duration} seconds from each audio...\n")

    cut_files = []

    for file in tqdm(mp3_files):

        try:
            audio = AudioSegment.from_mp3(file)

            clipped = audio[:duration * 1000]

            filename = os.path.basename(file)
            cut_path = f"{CUT_FOLDER}/cut_{filename}"

            clipped.export(cut_path, format="mp3")

            cut_files.append(cut_path)

        except Exception as e:
            print("Cut failed:", file)

    print("Cutting completed.\n")
    return cut_files


# ---------------------------
# Merge audio
# ---------------------------
def merge_audio(cut_files, output_file):

    print("\nMerging audio files...\n")

    final_audio = AudioSegment.empty()

    for file in tqdm(cut_files):
        audio = AudioSegment.from_mp3(file)
        final_audio += audio

    final_audio.export(output_file, format="mp3")

    print("\nMashup created successfully:", output_file)


# ---------------------------
# Validate CLI inputs
# ---------------------------
def validate_inputs():

    if len(sys.argv) != 5:

        print("\nInvalid arguments.")
        print("Usage:")
        print("python mashup_core.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>\n")

        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])

        if num_videos <= 0 or duration <= 0:
            raise ValueError

    except ValueError:

        print("Error: NumberOfVideos and AudioDuration must be positive integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if not output_file.endswith(".mp3"):
        print("Error: Output file must be .mp3 format")
        sys.exit(1)

    return singer, num_videos, duration, output_file


# ---------------------------
# Main
# ---------------------------
def main():

    print("\n===== YouTube Mashup Creator =====")

    singer, num_videos, duration, output_file = validate_inputs()

    try:

        setup_folders()

        videos = download_videos(singer, num_videos)

        mp3_files = convert_to_mp3(videos)

        cut_files = cut_audio(mp3_files, duration)

        merge_audio(cut_files, output_file)

        print("\nAll tasks completed successfully.")

    except Exception as e:
        print("\nError occurred:", str(e))


if __name__ == "__main__":
    main()
