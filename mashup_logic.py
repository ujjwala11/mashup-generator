from ut102317185 import setup_folders, download_videos, convert_to_mp3, cut_audio, merge_audio

def create_mashup(singer, num_videos, duration, output_file):

    print("Step 1: Setting up folders...", flush=True)
    setup_folders()

    print("Step 2: Downloading videos...", flush=True)
    videos = download_videos(singer, num_videos)

    print("Step 3: Cutting audio...", flush=True)
    cut_files = cut_audio(videos, duration)

    print("Step 4: Merging audio...", flush=True)
    merge_audio(cut_files, output_file)

    print("Mashup completed!", flush=True)

