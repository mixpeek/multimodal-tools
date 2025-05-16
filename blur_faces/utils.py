import cv2
import numpy as np
import os

# Attempt to load a common Haar cascade for face detection from OpenCV's data path
# This path might vary depending on the OpenCV installation.
HAAR_CASCADE_PATH_VARIANTS = [
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
    cv2.data.haarcascades + "haarcascade_frontalface_alt.xml",
    # Add more potential paths or a check if cv2.data.haarcascades is available
]
FACE_CASCADE = None
for path_var in HAAR_CASCADE_PATH_VARIANTS:
    if os.path.exists(path_var):
        FACE_CASCADE = cv2.CascadeClassifier(path_var)
        print(f"Loaded Haar cascade for face detection from: {path_var}")
        break

if FACE_CASCADE is None or FACE_CASCADE.empty():
    print("Error: Could not load Haar cascade for face detection. ")
    print(
        "Please ensure OpenCV is installed correctly and the cascade file is accessible."
    )
    # As a fallback, one might download it manually or point to a specific path.
    # For this script, we'll proceed, but face detection will fail.


def detect_faces(image_np, scale_factor=1.1, min_neighbors=5, min_size_px=30):
    """Detects faces in an image using the loaded Haar cascade."""
    if FACE_CASCADE is None or FACE_CASCADE.empty():
        # print("Warning: Face cascade not loaded. Skipping face detection.")
        return []
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(min_size_px, min_size_px),
    )
    return faces  # Returns list of (x, y, w, h)


def blur_face_region(image_np, x, y, w, h, kernel_size_tuple=(23, 23)):
    """Applies Gaussian blur to a specified region (face) of an image."""
    face_roi = image_np[y : y + h, x : x + w]
    if face_roi.size == 0:  # Avoid error if ROI is empty
        return
    # Ensure kernel size is odd
    k_w = (
        kernel_size_tuple[0]
        if kernel_size_tuple[0] % 2 == 1
        else kernel_size_tuple[0] + 1
    )
    k_h = (
        kernel_size_tuple[1]
        if kernel_size_tuple[1] % 2 == 1
        else kernel_size_tuple[1] + 1
    )

    blurred_face = cv2.GaussianBlur(face_roi, (k_w, k_h), 0)
    image_np[y : y + h, x : x + w] = blurred_face


def process_image_for_face_blur(
    image_path,
    output_path,
    blur_kernel_size=23,
    face_scale_factor=1.1,
    face_min_neighbors=5,
    face_min_size_px=30,
):
    """Loads an image, detects and blurs faces, and saves the result."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return False

    faces = detect_faces(
        img,
        scale_factor=face_scale_factor,
        min_neighbors=face_min_neighbors,
        min_size_px=face_min_size_px,
    )
    if (
        not FACE_CASCADE or FACE_CASCADE.empty()
    ):  # Check again in case it failed silently earlier
        print("Face detection cannot proceed as the cascade classifier is not loaded.")
        # Save the original image if face detection can't run to avoid errors
        # cv2.imwrite(output_path, img)
        # print(f"Saved original image to {output_path} as face detection module is not available.")
        return False  # Indicate failure to blur

    for x, y, w, h in faces:
        blur_face_region(
            img, x, y, w, h, kernel_size_tuple=(blur_kernel_size, blur_kernel_size)
        )

    try:
        cv2.imwrite(output_path, img)
        print(f"[✓] Blurred image saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving blurred image to {output_path}: {e}")
        return False


def process_video_for_face_blur(
    video_path,
    output_path,
    blur_kernel_size=23,
    face_scale_factor=1.1,
    face_min_neighbors=5,
    face_min_size_px=30,
):
    """Loads a video, detects and blurs faces in each frame, and saves the result."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return False

    if not FACE_CASCADE or FACE_CASCADE.empty():
        print(
            "Face detection cannot proceed as the cascade classifier is not loaded. Video processing aborted."
        )
        cap.release()
        return False

    # Get video properties for output
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Or use XVID, MJPG, etc.

    out_vid = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    print(f"Processing video {video_path} for face blurring...")
    frame_count = 0
    processed_frames_with_faces = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        faces = detect_faces(
            frame,
            scale_factor=face_scale_factor,
            min_neighbors=face_min_neighbors,
            min_size_px=face_min_size_px,
        )
        if len(faces) > 0:
            processed_frames_with_faces += 1
        for x, y, w, h in faces:
            blur_face_region(
                frame,
                x,
                y,
                w,
                h,
                kernel_size_tuple=(blur_kernel_size, blur_kernel_size),
            )

        out_vid.write(frame)
        if frame_count % 100 == 0:
            print(f"Processed {frame_count} frames...")

    cap.release()
    out_vid.release()
    print(f"\n[✓] Blurred video saved to {output_path}")
    print(f"Total frames processed: {frame_count}")
    print(
        f"Frames where faces were detected and blurred: {processed_frames_with_faces}"
    )
    return True
