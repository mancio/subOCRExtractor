
# Subtitle Extractor and Converter

This script automates the extraction of English subtitles from video files in formats such as `.mkv`, `.avi`, `.mp4`, and `.m4v`,
and converts them to `.srt` files using **MKVToolNix** and **Subtitle Edit**. The script supports multithreading, allowing multiple files to be processed concurrently.

## What is Subtitle Edit?

Subtitle Edit is a versatile, open-source tool primarily used for editing, synchronizing, and converting subtitle files.
It supports a wide range of subtitle formats and can perform various subtitle adjustments, such as merging lines, fixing time codes, and improving reading speed.
### Key Features
* Subtitle Conversion: Subtitle Edit allows you to convert between many subtitle formats, such as .srt, .sub, .vtt, .ass, and more.
* Synchronization and Editing: You can adjust timing and sync subtitles to match video audio. Subtitle Edit also provides tools for splitting or joining subtitle lines, adjusting reading speed, and enhancing legibility.
* Batch Processing: The tool supports batch conversion and editing, making it easy to apply adjustments to multiple files at once.

## OCR (Optical Character Recognition)
One of Subtitle Edit's standout features is its OCR (Optical Character Recognition) capability, 
which is particularly useful for extracting subtitle text embedded in images (such as from DVDs or Blu-rays where subtitles are stored as bitmap images rather than text).
Subtitle Edit uses OCR engines like Tesseract or nOCR to recognize text in these images and convert it into editable subtitle text,
which can then be saved as an .srt or another text-based subtitle format.
The OCR process can be somewhat time-intensive, as it relies on analyzing each frame or image file, especially for longer videos. However, 
by combining Subtitle Edit's built-in OCR tools with engines like Tesseract, users can achieve high accuracy in subtitle conversion from image-based sources.

## Requirements

- **MKVToolNix**: Install [MKVToolNix](https://mkvtoolnix.download/) and ensure `mkvextract.exe` is accessible.
- **Subtitle Edit**: Install [Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit) and confirm `SubtitleEdit.exe` is accessible.

### Configurable Paths
Define paths to `mkvextract.exe` and `SubtitleEdit.exe` in the script:
```python
mkvextract_path = r"C:\Program Files\MKVToolNix\mkvextract.exe"
subtitle_edit_cli = r"C:\Program Files\Subtitle Edit\SubtitleEdit.exe"
```

### Concurrent Threads
You can set the number of concurrent threads to control parallel processing:
```python
max_threads = 10  # Set the number of concurrent threads here
```

## Usage

To run the script, use the following command:
```bash
python script.py <input_folder>
```
Replace `<input_folder>` with the path to the folder containing your video files.

### Optional Variables
- **`manual`**: Set to `True` to manually specify a subtitle track (default is `False`).
- **`subtitle_track_to_keep`**: If `manual` is `True`, specify the track ID to keep (default is `2`).

## How It Works

1. **Track Identification**:
   - For each video file, the script identifies audio and subtitle tracks using `mkvmerge`.
   - If an English subtitle track is detected, its track ID is saved for extraction.

2. **Subtitle Extraction**:
   - Using `mkvextract`, the script extracts the English subtitle track, saved as `.idx` and `.sub` files.
   - After extraction, the script confirms both files exist before conversion.

3. **Conversion to SRT**:
   - The script converts `.sub` files to `.srt` format using `Subtitle Edit`.
   - The converted `.srt` files are saved in the same directory as the original video file.

## Functions

- **identify_and_parse_tracks(file_path)**: Identifies tracks within the video file, focusing on English subtitle tracks, and returns their track IDs.
- **extract_and_convert_subtitle(input_path, subtitle_track_id)**: Extracts subtitle tracks using `mkvextract` and converts them to `.srt` using `Subtitle Edit`.
- **process_files(input_folder, manual, subtitle_track_to_keep, max_threads)**: Processes all video files in the folder concurrently, handling track identification, extraction, and conversion.

## Example

To process a folder of videos automatically:

```bash
python script.py "C:\path\to\video_folder"
```

For manual track selection:

1. Set `manual = True` in the script.
2. Adjust `subtitle_track_to_keep` to the desired track ID.

## Error Handling

The script includes error handling for:
- Missing or incorrect paths for `mkvextract` and `Subtitle Edit`.
- Failed subtitle extraction and conversion attempts.
- Missing `.idx` and `.sub` files after extraction.

## Dependencies

Ensure `MKVToolNix` and `Subtitle Edit` are properly installed and the paths are correctly set in the script.
