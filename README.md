# 🧰 Multimodal Tools

A collection of simple, standalone Python scripts for working with **video, audio, image, and text** data — designed for developers exploring multimodal AI.

Each utility lives in its own folder with examples and a CLI-friendly interface.

---

## 📂 Tools (WIP)

| Tool | Description |
|------|-------------|
| [`segment_transcript_by_topic/`](./segment_transcript_by_topic) | Transcribe and cluster audio/video by topic |
| [`split_video_by_second/`](./split_video_by_second) | Split a video file into N-second chunks |
| [`extract_thumbnails/`](./extract_thumbnails) | Grab frames from a video every N seconds |
| [`transcribe_audio/`](./transcribe_audio) | Transcribe audio using Whisper |
| [`search_local_media/`](./search_local_media) | CLIP-based text search across your media folder |
| [`scene_change_split/`](./scene_change_split) | Splits a video into separate clips based on detected scene changes. |
| [`caption_search/`](./caption_search) | Searches for text within video captions or existing Whisper transcripts. |
| [`generate_video_captions/`](./generate_video_captions) | Generates SRT/VTT caption files from video or audio using Whisper. |
| [`video_shot_segmenter/`](./video_shot_segmenter) | Segments a video into individual shots based on visual changes. |
| [`summarize_transcript/`](./summarize_transcript) | Summarizes text from a transcript file (e.g., from Whisper output). |
| [`blur_faces/`](./blur_faces) | Detects and blurs faces in images or video frames for privacy. |

---

## 🛠️ Getting Started

```bash
# Clone the repo
git clone https://github.com/mixpeek/multimodal-tools.git
cd multimodal-tools

# Pick a tool and follow its README
cd segment_transcript_by_topic
pip install -r requirements.txt
python segment_transcript.py --input path/to/video.mp4
```

---

## 🚀 Why use these?

Multimodal content is everywhere — but tooling is scattered. This repo brings together focused, no-dependency-heavy scripts to help you get things done without setting up complex pipelines.

Ideal for:
- Prototyping and experimentation
- Content analysis workflows
- ML/AI feature extraction
- Exploring retrieval use cases

---

## 🔌 Looking for hosted feature extractors?

If you want to scale beyond local scripts, [Mixpeek](https://mixpeek.com/extractors) offers managed, production-ready multimodal extractors (video, image, audio, and more) you can plug into your stack.

___

## 🤝 Contributing
Want to add a new tool or improve an existing one? PRs welcome.



