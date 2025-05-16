## 🧠 Segment Transcript by Topic

This Python tool accepts a video or audio file, transcribes it using OpenAI Whisper, embeds transcript segments using SentenceTransformers, and clusters them by topic using HDBSCAN.

### 🔧 Features
- Automatic speech transcription (Whisper)
- Sentence segmentation
- Embedding via SentenceTransformers
- Clustering via HDBSCAN
- Topic summary generation (optional)

### 🏁 Quickstart
```bash
# Install deps
pip install -r requirements.txt

# Run segmentation
python segment_transcript.py --input examples/sample_video.mp4 --output segments.json
```

### 📂 Output Format
```json
[
  {
    "topic_id": 0,
    "start": 12.3,
    "end": 54.6,
    "text": "Discussion about industry challenges..."
  },
  ...
]
``` 