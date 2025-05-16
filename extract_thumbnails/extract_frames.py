import argparse
import ffmpeg
import os
import math


def get_video_duration(input_path):
    """Gets the duration of a video file in seconds using ffprobe."""
    try:
        probe = ffmpeg.probe(input_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        if video_stream and "duration" in video_stream:
            return float(video_stream["duration"])
        if "format" in probe and "duration" in probe["format"]:
            return float(probe["format"]["duration"])
        raise ValueError("Could not determine video duration.")
    except ffmpeg.Error as e:
        print(f"Error probing video: {e.stderr.decode('utf8')}")
        raise


def format_time(seconds):
    """Formats seconds into HhMmSs string for filenames."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}h{m:02d}m{s:02d}s"


def extract_frames_at_interval(input_path, output_folder, interval_seconds):
    """Extracts frames from the video at specified N-second intervals."""
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")

    total_duration = get_video_duration(input_path)
    if total_duration == 0:
        print(
            "Error: Video duration is 0 or could not be determined. Cannot extract frames."
        )
        return

    print(
        f"Video duration: {total_duration:.2f}s. Extracting frames every {interval_seconds}s."
    )

    frame_count = 0
    for i in range(0, math.ceil(total_duration), interval_seconds):
        current_time_sec = i
        if current_time_sec > total_duration:  # Ensure we don't go past the end
            break

        # Use a timestamp-based filename for clarity, or a sequential one
        # timestamp_str = format_time(current_time_sec)
        # output_filename = os.path.join(output_folder, f"frame_at_{timestamp_str}.jpg")
        frame_count += 1
        output_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.jpg")

        print(
            f"Extracting frame {frame_count} at {current_time_sec:.2f}s -> {output_filename}"
        )

        try:
            (
                ffmpeg.input(
                    input_path, ss=current_time_sec
                )  # Seek to the specific time
                .output(
                    output_filename, vframes=1, format="image2", vcodec="mjpeg"
                )  # Extract one frame
                .global_args("-loglevel", "error")  # Suppress verbose ffmpeg logs
                .run(overwrite_output=True)
            )
            print(f"[✓] Saved {output_filename}")
        except ffmpeg.Error as e:
            print(
                f"Error extracting frame at {current_time_sec:.2f}s: {e.stderr.decode('utf8')}"
            )
            print(f"[✗] Failed to save {output_filename}")

    if frame_count == 0 and total_duration > 0:
        print(
            "No frames were extracted. Check interval and video length. Attempting to extract first frame if interval > duration."
        )
        # As a fallback, if interval is larger than duration, extract the first frame.
        if interval_seconds > total_duration:
            output_filename = os.path.join(output_folder, f"frame_00001.jpg")
            try:
                (
                    ffmpeg.input(input_path, ss=0)
                    .output(output_filename, vframes=1, format="image2", vcodec="mjpeg")
                    .global_args("-loglevel", "error")
                    .run(overwrite_output=True)
                )
                print(f"[✓] Saved first frame as fallback: {output_filename}")
            except ffmpeg.Error as e:
                print(
                    f"Error extracting first frame as fallback: {e.stderr.decode('utf8')}"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract frames from a video at N-second intervals."
    )
    parser.add_argument("--input", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--output_folder", required=True, help="Directory to save the extracted frames."
    )
    parser.add_argument(
        "--interval",
        type=int,
        required=True,
        help="Interval in seconds between frame extractions.",
    )

    args = parser.parse_args()

    if args.interval <= 0:
        print("Error: Interval must be a positive integer.")
    else:
        extract_frames_at_interval(args.input, args.output_folder, args.interval)
        print("Frame extraction process completed.")
