import argparse
import os
import scenedetect
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector, ThresholdDetector
from scenedetect.video_splitter import split_video_ffmpeg


def segment_video_into_shots(
    video_path,
    output_folder,
    detector_type="content",
    threshold=27.0,
    min_shot_len_frames=15,
):
    """Detects shots in a video and splits it into clips for each shot."""
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
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()

        if detector_type == "content":
            # ContentDetector is often good for finding cuts and significant changes.
            # The threshold here would be similar to scene detection, but shot boundaries
            # are often more frequent. Lower threshold = more sensitive.
            # min_scene_len (in frames) can also be used to avoid very short shots.
            scene_manager.add_detector(
                ContentDetector(threshold=threshold, min_scene_len=min_shot_len_frames)
            )
            print(
                f"Using ContentDetector with threshold: {threshold}, min shot length (frames): {min_shot_len_frames}"
            )
        elif detector_type == "threshold":
            # ThresholdDetector looks for changes in average frame intensity.
            # Can be very sensitive. Good for fast cuts if tuned well.
            scene_manager.add_detector(
                ThresholdDetector(
                    threshold=threshold, min_scene_len=min_shot_len_frames
                )
            )
            print(
                f"Using ThresholdDetector with threshold: {threshold}, min shot length (frames): {min_shot_len_frames}"
            )
        else:
            print(
                f"Error: Unknown detector type '{detector_type}'. Use 'content' or 'threshold'."
            )
            return

        video_manager.set_downscale_factor()  # Improves performance

        print(f"Starting video processing and shot detection for {video_path}...")
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        shot_list = (
            scene_manager.get_scene_list()
        )  # PySceneDetect uses 'scene' terminology generically

        print(f"Found {len(shot_list)} shots.")

        if not shot_list:
            print(
                "No shots detected. Check video content or adjust detector settings/threshold."
            )
            video_manager.release()
            return

        print(f"Splitting video into shots and saving to {output_folder}...")
        # Using a different naming template for shots
        split_video_ffmpeg(
            shot_list,
            video_manager,
            output_dir=output_folder,
            file_name_template="$VIDEO_NAME-shot-$SCENE_NUMBER",
            show_progress=True,
            suppress_output=False,
        )

        print("[✓] Video splitting into shots complete.")

    except Exception as e:
        print(f"An error occurred during shot detection or splitting: {e}")
    finally:
        if "video_manager" in locals() and video_manager.is_started():
            video_manager.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a video into clips based on detected shots."
    )
    parser.add_argument("--input", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--output_folder", required=True, help="Directory to save the shot clips."
    )
    parser.add_argument(
        "--detector",
        type=str,
        default="content",
        choices=["content", "threshold"],
        help="Detector type to use: 'content' (default) or 'threshold'.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=27.0,
        help="Detection threshold. For ContentDetector (default 27.0, lower is more sensitive). For ThresholdDetector (e.g., 10-30, depends on video). ",
    )
    parser.add_argument(
        "--min_shot_len",
        type=int,
        default=15,
        help="Minimum shot length in frames (default: 15). Shorter detected shots will be merged.",
    )

    args = parser.parse_args()

    segment_video_into_shots(
        args.input, args.output_folder, args.detector, args.threshold, args.min_shot_len
    )
