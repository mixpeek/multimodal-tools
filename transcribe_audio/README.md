# 🎤 Transcribe Audio with Whisper

This Python tool transcribes audio or video files using OpenAI's Whisper model. It can extract audio from video files before transcription.

### 🔧 Features
- Transcribes audio from various audio and video formats.
- Uses OpenAI Whisper for high-quality transcription.
- Outputs transcription as a JSON file, including segments with timestamps.
- Option to specify Whisper model size.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Transcribe an audio file
python transcribe_script.py --input examples/sample_audio.mp3 --output transcript.json

# Transcribe a video file (audio will be extracted first)
python transcribe_script.py --input examples/sample_video.mp4 --output video_transcript.json --model_size base
```

### 📂 Output Format (JSON)
```json
{
  "text": "Full transcribed text...",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 5.32,
      "text": "Hello, this is a test.",
      "tokens": [ ... ],
      "temperature": 0.0,
      "avg_logprob": -0.5,
      "compression_ratio": 1.2,
      "no_speech_prob": 0.1
    },
    ...
  ],
  "language": "en"
}
``` 