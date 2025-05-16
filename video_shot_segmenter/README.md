# 🎞️ Segment Video by Shots

This Python tool analyzes a video file, detects individual shots (e.g., camera cuts, quick transitions within a scene), and splits the video into clips for each detected shot. It primarily uses PySceneDetect, potentially with settings tuned for shot detection rather than broader scene changes.

### 🔧 Features
- Automatic shot boundary detection.
- Splits the original video into multiple smaller clips, one for each shot.
- Outputs shot clips to a specified folder (e.g., `shot_0001.mp4`).
- Options to adjust detection sensitivity (e.g., using threshold with `ThresholdDetector` or parameters for `ContentDetector`).

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Make sure ffmpeg is installed and accessible in your PATH

# Run shot segmentation (default uses ContentDetector, often good for cuts)
python shot_segmenter_script.py --input examples/sample_video.mp4 --output_folder output_shots/

# Example using ThresholdDetector (might be better for very fast cuts or specific thresholding needs)
python shot_segmenter_script.py --input examples/sample_video.mp4 --output_folder output_shots_threshold/ --detector threshold --threshold 15
```

### ⚙️ How it Works
1.  The video is loaded using `PySceneDetect`'s `VideoManager`.
2.  A detector like `ContentDetector` (good for detecting cuts) or `ThresholdDetector` (sensitive to frame-to-frame pixel intensity changes) is used. The parameters for these detectors can be adjusted for shot-level granularity.
3.  `PySceneDetect` identifies the start and end timecodes for each shot.
4.  The video is then split into individual shot clips using `ffmpeg` (typically called by `PySceneDetect`'s splitting utilities).

### 📂 Output
The tool creates an output folder (e.g., `output_shots/`) containing video clips for each detected shot, named sequentially:
- `shot_0001.mp4`
- `shot_0002.mp4`
- ...

**Note**: The distinction between a "shot" and a "scene" can be subjective. This tool aims for more granular segmentation (shots) compared to the `scene_change_split` tool which targets broader narrative scenes. 