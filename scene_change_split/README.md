# 🎬 Split Video by Scene Changes

This Python tool analyzes a video file, detects scene changes, and splits the video into individual clips for each detected scene. It leverages the PySceneDetect library for robust scene detection and FFmpeg for video splitting.

### 🔧 Features
- Automatic scene change detection using content-aware analysis.
- Splits the original video into multiple smaller clips, one for each scene.
- Outputs scene clips to a specified folder with sequential naming (e.g., `scene_001.mp4`).
- Option to adjust the detection threshold for sensitivity control.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Make sure ffmpeg is installed and accessible in your PATH
# (PySceneDetect often relies on the ffmpeg CLI for splitting)

# Run scene splitting
python scene_change_splitter.py --input examples/sample_video.mp4 --output_folder output_scenes/

# Adjust threshold (default is 27.0, lower is more sensitive)
python scene_change_splitter.py --input examples/sample_video.mp4 --output_folder output_scenes_sensitive/ --threshold 20
```

### ⚙️ How it Works
1.  The video is loaded using `PySceneDetect`.
2.  A `ContentDetector` (or `ThresholdDetector`) is used to find significant changes between frames, indicating scene breaks.
3.  The list of detected scenes (start and end times) is obtained.
4.  `PySceneDetect`'s video splitting capability (which often uses `ffmpeg` command-line tool) is then used to create individual video files for each scene.

### 📂 Output
The tool will create an output folder (e.g., `output_scenes/`) containing video clips for each detected scene, named like:
- `scene_001.mp4`
- `scene_002.mp4`
- ... 