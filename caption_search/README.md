# 🔎 Search Video Captions for Text

This Python tool transcribes a video file (if needed) and then searches for specific text queries within its captions/transcript. It helps you quickly find moments in a video where certain words or phrases are spoken.

### 🔧 Features
- Transcribes video using OpenAI Whisper to get time-coded caption segments.
- Searches for exact text matches within the transcribed segments.
- Outputs the start and end times of video segments where the query text is found.
- Option to use an existing transcript file (e.g., JSON from Whisper).

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Search within a video (will transcribe first)
python search_captions.py --video_input examples/sample_video.mp4 --query "hello world"

# Search using a pre-existing Whisper JSON transcript
# (First, generate a transcript if you don't have one)
# python some_transcription_script.py --input examples/sample_video.mp4 --output examples/transcript.json
python search_captions.py --transcript_input examples/sample_transcript.json --query "important announcement"
```

### ⚙️ How it Works
1.  **Transcription (if needed)**: If a video file is provided directly, its audio is extracted and transcribed using OpenAI Whisper. This produces a list of text segments, each with a start and end timestamp.
2.  **Load Transcript**: If a pre-existing transcript file (Whisper JSON format) is provided, it's loaded directly.
3.  **Search**: The tool iterates through the text of each caption segment and performs a case-insensitive search for the provided query string.
4.  **Output**: For every segment where the query is found, the tool prints the source file, the start time, end time, and the text of that segment.

### 📂 Output Format (Console)
```
Found query "hello world" in 'examples/sample_video.mp4':
- Segment (0m10.52s - 0m15.88s): "... and then I said hello world to everyone ..."
- Segment (1m2s.10s - 1m5s.0s): "So, to conclude, hello world."

Found query "important announcement" in 'examples/sample_transcript.json':
- Segment (0m50.0s - 0m55.0s): "Now for an important announcement regarding the project."
``` 