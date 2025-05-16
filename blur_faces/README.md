# 😶 Blur Faces in Images and Videos

This Python tool detects faces in images (JPEG, PNG) and videos (MP4, AVI, etc.) and applies a blurring effect to them. It's useful for privacy protection and redacting faces in media.

### 🔧 Features
- Detects faces in static images and individual video frames.
- Applies a Gaussian blur to the detected facial regions.
- Supports various image and video formats (those readable by OpenCV).
- Outputs a new image/video file with faces blurred.
- Option to adjust blur intensity and face detection parameters.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Blur faces in an image
python blur_faces_script.py --input examples/sample_image_with_faces.jpg --output examples/blurred_image.jpg

# Blur faces in a video
python blur_faces_script.py --input examples/sample_video_with_faces.mp4 --output examples/blurred_video.mp4

# Adjust blur intensity (kernel size, must be odd)
python blur_faces_script.py --input examples/sample_image_with_faces.jpg --output examples/blurred_image_strong.jpg --blur_kernel 51
```

### ⚙️ How it Works
1.  **Load Media**: The input image or video is loaded using OpenCV.
2.  **Face Detection**: For each image or video frame:
    *   A pre-trained face detection model (e.g., Haar cascade or a DNN from OpenCV's Zoo) is used to identify face regions.
3.  **Blurring**: A Gaussian blur is applied to each detected face bounding box.
4.  **Output**: 
    *   For images, the modified image with blurred faces is saved.
    *   For videos, each frame is processed, and a new video is encoded and saved with the blurred faces.

### 📂 Output
-   If the input is an image, an image file with blurred faces is created.
-   If the input is a video, a new video file with faces blurred throughout is created. 