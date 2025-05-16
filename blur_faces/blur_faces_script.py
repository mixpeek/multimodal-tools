import argparse
import os
import cv2  # For checking if input is image or video based on read/open success
from utils import process_image_for_face_blur, process_video_for_face_blur, FACE_CASCADE


def is_image_file(filepath):
    """Checks if the filepath is likely an image file that OpenCV can read."""
    # Basic check, can be expanded with more explicit extensions
    img = cv2.imread(filepath)
    if img is not None:
        return True
    return False


def is_video_file(filepath):
    """Checks if the filepath is likely a video file that OpenCV can open."""
    cap = cv2.VideoCapture(filepath)
    if cap.isOpened():
        cap.release()
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Detect and blur faces in images or videos."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the input image or video file."
    )
    parser.add_argument(
        "--output", required=True, help="Path to save the output processed file."
    )
    parser.add_argument(
        "--blur_kernel",
        type=int,
        default=23,
        help="Size of the Gaussian blur kernel (must be odd, e.g., 23, 51). Larger is more blur. Default: 23.",
    )
    parser.add_argument(
        "--face_scale_factor",
        type=float,
        default=1.1,
        help="Scale factor for Haar cascade face detection (default: 1.1). How much the image size is reduced at each image scale.",
    )
    parser.add_argument(
        "--face_min_neighbors",
        type=int,
        default=5,
        help="Minimum neighbors for Haar cascade face detection (default: 5). How many neighbors each candidate rectangle should have to retain it.",
    )
    parser.add_argument(
        "--face_min_size_px",
        type=int,
        default=30,
        help="Minimum possible face size in pixels for Haar cascade (default: 30).",
    )
    args = parser.parse_args()

    if not (FACE_CASCADE and not FACE_CASCADE.empty()):
        print(
            "Critical Error: Face detection model (Haar cascade) could not be loaded from utils.py. Aborting."
        )
        print(
            "Please ensure OpenCV is installed correctly and 'haarcascade_frontalface_default.xml' is accessible."
        )
        return

    if not os.path.exists(args.input):
        print(f"Error: Input file not found at {args.input}")
        return

    # Ensure blur kernel is odd
    blur_k = args.blur_kernel
    if blur_k % 2 == 0:
        blur_k += 1
        print(f"Blur kernel size was even, adjusted to {blur_k}")

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Determine if input is an image or video
    if is_image_file(args.input):
        print(f"Processing {args.input} as an image.")
        process_image_for_face_blur(
            args.input,
            args.output,
            blur_kernel_size=blur_k,
            face_scale_factor=args.face_scale_factor,
            face_min_neighbors=args.face_min_neighbors,
            face_min_size_px=args.face_min_size_px,
        )
    elif is_video_file(args.input):
        print(f"Processing {args.input} as a video.")
        process_video_for_face_blur(
            args.input,
            args.output,
            blur_kernel_size=blur_k,
            face_scale_factor=args.face_scale_factor,
            face_min_neighbors=args.face_min_neighbors,
            face_min_size_px=args.face_min_size_px,
        )
    else:
        print(
            f"Error: Could not determine if {args.input} is a supported image or video file, or file is corrupted."
        )


if __name__ == "__main__":
    main()
