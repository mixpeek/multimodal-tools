# ✍️ Generate Video/Audio Captions (SRT, VTT)

This Python tool transcribes a video or audio file using OpenAI Whisper and generates caption files in common formats like SRT (.srt) and WebVTT (.vtt).

### 🔧 Features
- Transcribes video or audio files using OpenAI Whisper.
- Outputs caption files in SRT and VTT formats.
- Automatically names output files based on the input file name.
- Option to specify Whisper model size for transcription.
- Option to specify output directory for caption files.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Generate captions for a video file
python generate_captions_script.py --input examples/sample_video.mp4

# Generate captions for an audio file and specify output directory
python generate_captions_script.py --input examples/sample_audio.mp3 --output_dir custom_captions/

# Specify a different Whisper model
python generate_captions_script.py --input examples/sample_video.mp4 --model_size small
```

### ⚙️ How it Works
1.  **Audio Extraction (if video)**: If a video file is provided, its audio is extracted into a temporary file suitable for Whisper.
2.  **Transcription**: The audio is transcribed using OpenAI Whisper, which provides timed segments of text.
3.  **Caption Formatting**: The timed segments from Whisper are formatted into SRT and VTT caption strings.
4.  **File Output**: The formatted caption strings are saved as `.srt` and `.vtt` files in the specified output directory (or alongside the input file by default).

### 📂 Output Files
For an input file named `my_video.mp4`, the tool will generate:
- `my_video.srt`
- `my_video.vtt`

These files will be placed in the same directory as the input file, or in the directory specified by `--output_dir`. 