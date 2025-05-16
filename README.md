# 🧰 Multimodal Tools

A collection of simple, standalone Python scripts for working with **video, audio, image, and text** data — designed for developers exploring multimodal AI.

Each utility lives in its own folder with examples and a CLI-friendly interface.

---

## 🚀 Why use these?

Multimodal content is everywhere — but tooling is scattered. This repo brings together focused, no-dependency-heavy scripts to help you get things done without setting up complex pipelines.

Ideal for:
- Prototyping and experimentation
- Content analysis workflows
- ML/AI feature extraction
- Exploring retrieval use cases

---

## 📂 Tools (WIP)

| Tool | Description |
|------|-------------|
| [`segment_transcript_by_topic/`](./segment_transcript_by_topic) | Transcribe and cluster audio/video by topic |
| [`split_video_by_second/`](./split_video_by_second) | Split a video file into N-second chunks |
| [`extract_thumbnails/`](./extract_thumbnails) | Grab frames from a video every N seconds |
| [`transcribe_audio/`](./transcribe_audio) | Transcribe audio using Whisper |
| [`search_local_media/`](./search_local_media) | CLIP-based text search across your media folder |
| [`scene_change_split/`](./scene_change_split) | Introduces users to segmentation — essential for indexing and retrieval, ties into Mixpeek pipelines. |
| [`caption_search/`](./caption_search) | Text-based video retrieval is sticky. Very relatable problem for creators + brands. |
| [`generate_video_captions/`](./generate_video_captions) | Popular Whisper wrapper, easy way in. Can upsell with "hosted + searchable." |
| [`video_shot_segmenter/`](./video_shot_segmenter) | Gets technical users thinking in terms of shots + segments. Good primer. |
| [`summarize_transcript/`](./summarize_transcript) | Pairs well with your retrieval infra, especially if you show concept search. |
| [`blur_faces/`](./blur_faces) | Niche use case (privacy, redaction). Could be relevant for security clients though. |

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

## 🔌 Looking for hosted feature extractors?

If you want to scale beyond local scripts, [Mixpeek](https://mixpeek.com/extractors) offers managed, production-ready multimodal extractors (video, image, audio, and more) you can plug into your stack.

___

## 🤝 Contributing
Want to add a new tool or improve an existing one? PRs welcome.



