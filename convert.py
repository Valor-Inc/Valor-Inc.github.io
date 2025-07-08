import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Number of parallel conversions (adjust for your CPU)
NUM_THREADS = 8

def convert_mp3_to_wav(mp3_path):
    wav_path = os.path.splitext(mp3_path)[0] + '.wav'
    if os.path.exists(wav_path):
        print(f"[SKIP] {wav_path} already exists.")
        return
    print(f"[CONVERT] {mp3_path} -> {wav_path}")
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', mp3_path, '-c:a', 'pcm_s16le', wav_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        print(f"[ERROR] Failed to convert {mp3_path}:\n{result.stderr.decode()}")
    else:
        print(f"[DONE] {wav_path}")

def find_mp3_files(root='.'):
    mp3_files = []
    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.lower().endswith('.mp3'):
                mp3_files.append(os.path.join(dirpath, file))
    return mp3_files

if __name__ == "__main__":
    mp3_files = find_mp3_files('.')
    print(f"Found {len(mp3_files)} mp3 files.")

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(convert_mp3_to_wav, mp3) for mp3 in mp3_files]
        for future in as_completed(futures):
            pass  # All output is handled in the worker function
