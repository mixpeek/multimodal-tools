# ✂️ Split Video by N Seconds

This Python tool splits a video file into multiple smaller video clips, each of a specified duration in seconds. It uses FFmpeg for efficient video processing.

### 🔧 Features
- Splits video into N-second chunks.
- Supports various video formats (any format FFmpeg can handle).
- Customizable chunk duration.
- Outputs chunks to a specified folder with sequential naming.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Run splitting
python split_video.py --input examples/sample_video.mp4 --output_folder output_chunks/ --duration 10
```

### 📂 Output
The tool will create an output folder (e.g., `output_chunks/`) containing the video segments named sequentially, like:
- `chunk_001.mp4`
- `chunk_002.mp4`
- ...

The last chunk might be shorter than the specified duration if the total video length is not an exact multiple of the chunk duration. 