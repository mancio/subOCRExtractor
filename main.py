import os
import sys
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global path to mkvextract and Subtitle Edit CLI
mkvextract_path = r"C:\Program Files\MKVToolNix\mkvextract.exe"
subtitle_edit_cli = r"C:\Program Files\Subtitle Edit\SubtitleEdit.exe"

# Set the number of concurrent threads to control parallel processing
max_threads = 10  # Adjust this value as needed


def identify_and_parse_tracks(file_path):
    """
    Identifies audio and subtitle tracks in the video file and returns their IDs.
    """
    cmd = [mkvextract_path.replace('mkvextract', 'mkvmerge'), "--identify", "--identification-format", "json", file_path]

    last_english_subtitle_track_id = None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)
        track_info = json.loads(result.stdout)

        print(f"Track information for {file_path}:")

        for track in track_info.get('tracks', []):
            track_id = track.get('id', 'N/A')
            track_lang = track['properties'].get('language_ietf', track['properties'].get('language', 'und'))
            track_type = track['type']

            print(f"  - Track ID: {track_id}, Type: {track_type}, Language: {track_lang}")

            # If the track is a subtitle and in English, store the ID
            if track_type == 'subtitles' and 'en' in track_lang:
                last_english_subtitle_track_id = track_id

    except subprocess.CalledProcessError as e:
        print(f"Error while identifying tracks: {e}")

    return last_english_subtitle_track_id


def extract_and_convert_subtitle(input_path, subtitle_track_id):
    """
    Extracts subtitle tracks using mkvextract and converts the extracted idx/sub to srt using Subtitle Edit.
    """
    base_name = os.path.splitext(input_path)[0]
    idx_file = base_name + ".idx"
    sub_file = base_name + ".sub"
    output_srt = base_name + ".srt"

    # Use mkvextract to extract the subtitle track (VobSub might be extracted as .idx/.sub)
    cmd_extract = [
        mkvextract_path,
        "tracks",
        input_path,
        f"{subtitle_track_id}:{idx_file}"
    ]

    try:
        # Run extraction and wait until it completes
        subprocess.run(cmd_extract, check=True)
        print(f"Extracted subtitle for {input_path} to {idx_file} and {sub_file}")

        # Confirm existence of both .idx and .sub files before conversion
        if os.path.exists(idx_file) and os.path.exists(sub_file):
            # Convert to SRT using Subtitle Edit
            cmd_convert = [
                subtitle_edit_cli,
                '/convert',
                sub_file,  # Use sub_file as input for conversion
                'srt',     # Specifies the output format
                '/outputfilename:' + output_srt
            ]
            subprocess.run(cmd_convert, check=True)
            print(f"Converted {idx_file} and {sub_file} to {output_srt}")
        else:
            print(f"Subtitle extraction failed for {input_path} (missing .idx/.sub files).")
    except subprocess.CalledProcessError as e:
        print(f"Error processing subtitle extraction and conversion for {input_path}: {e}")


def process_file(input_path, manual, subtitle_track_to_keep):
    """
    Processes a single file for subtitle extraction and conversion.
    """
    # Automatically detect subtitle tracks unless manual mode is set to True
    if not manual:
        subtitle_track_to_keep = identify_and_parse_tracks(input_path)
        print(f"I will keep Track ID: {subtitle_track_to_keep} for subtitles")
    else:
        identify_and_parse_tracks(input_path)

    # Proceed with subtitle extraction and conversion
    if subtitle_track_to_keep:
        extract_and_convert_subtitle(input_path, subtitle_track_to_keep)
    else:
        print(f"No English subtitle track found for {input_path}.")


def process_files(input_folder, manual, subtitle_track_to_keep, max_threads):
    """
    Processes all files in the folder and extracts/converts subtitles to SRT using multiple threads.
    """
    # Collect all video files in the directory
    video_files = [
        os.path.join(input_folder, filename)
        for filename in os.listdir(input_folder)
        if filename.lower().endswith((".avi", ".mkv", ".mp4", ".m4v"))
    ]

    # Process files concurrently with a thread pool
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_file = {
            executor.submit(process_file, file, manual, subtitle_track_to_keep): file
            for file in video_files
        }

        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as exc:
                print(f"{file} generated an exception: {exc}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    manual = False  # Set to True if you want to manually specify tracks
    subtitle_track_to_keep = 2  # This will be used if manual is True

    process_files(input_folder, manual, subtitle_track_to_keep, max_threads)
