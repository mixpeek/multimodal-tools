# 🖼️ Extract Frames from Video

This Python tool extracts frames (thumbnails) from a video file at specified N-second intervals. It uses FFmpeg for efficient video processing.

### 🔧 Features
- Extracts frames from a video at regular N-second intervals.
- Supports various video formats (any format FFmpeg can handle).
- Customizable interval.
- Outputs frames to a specified folder, named by timestamp or sequence.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Run frame extraction
python extract_frames.py --input examples/sample_video.mp4 --output_folder output_frames/ --interval 5
```

### 📂 Output
The tool will create an output folder (e.g., `output_frames/`) containing the extracted frames named sequentially or by timestamp, like:
- `frame_00001.jpg` (sequential)
- `frame_at_0m5s.jpg` (timestamp based)
- ... 