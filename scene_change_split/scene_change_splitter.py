import argparse
import os
import scenedetect
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import (
    split_video_ffmpeg,
)  # For splitting based on detected scenes


def split_video_by_scenes(video_path, output_folder, threshold):
    """Detects scenes in a video and splits it into clips for each scene."""
    if not os.path.exists(video_path):
        print(f"Error: Input video not found at {video_path}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    else:
        print(
            f"Output directory {output_folder} already exists. Files may be overwritten."
        )

    try:
        # Create a video_manager point to video file
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()

        # Add ContentDetector algorithm (alternatively, ThresholdDetector can be used)
        scene_manager.add_detector(ContentDetector(threshold=threshold))

        # Base video_manager CLI progress bar disabled by default.
        # Enable it here to show progress while processing the video.
        video_manager.set_downscale_factor()

        print(f"Starting video processing and scene detection for {video_path}...")
        # Start video_manager.
        video_manager.start()

        # Perform scene detection.
        scene_manager.detect_scenes(frame_source=video_manager)

        # Obtain list of detected scenes (Timecode objects).
        scene_list = scene_manager.get_scene_list()
        # Each scene in scene_list is a tuple of (Start Timecode, End Timecode).

        print(f"Found {len(scene_list)} scenes.")

        if not scene_list:
            print("No scenes detected. Check video content or adjust threshold.")
            video_manager.release()
            return

        # Use PySceneDetect's utility to split the video using ffmpeg.
        # This requires ffmpeg to be installed and in the system PATH.
        print(f"Splitting video into scenes and saving to {output_folder}...")
        # split_video_ffmpeg expects a list of scene tuples (start_time, end_time)
        # and the video_manager object.
        # The output files will be named scene-001.mp4, scene-002.mp4, etc. by default.
        # We can customize the output file name format if needed using file_name_template.
        split_video_ffmpeg(
            scene_list,
            video_manager,
            output_dir=output_folder,
            show_progress=True,
            suppress_output=False,
        )  # show_progress for ffmpeg splitting

        print("[✓] Video splitting complete.")

    except Exception as e:
        print(f"An error occurred during scene detection or splitting: {e}")
    finally:
        if "video_manager" in locals() and video_manager.is_started():
            video_manager.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a video into clips based on scene changes."
    )
    parser.add_argument("--input", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--output_folder", required=True, help="Directory to save the scene clips."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=27.0,
        help="Detection threshold for ContentDetector (default: 27.0). Lower values are more sensitive to changes.",
    )

    args = parser.parse_args()

    split_video_by_scenes(args.input, args.output_folder, args.threshold)
