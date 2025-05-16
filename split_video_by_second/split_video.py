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
        # Fallback for containers where duration might be in format tags
        if "format" in probe and "duration" in probe["format"]:
            return float(probe["format"]["duration"])
        raise ValueError("Could not determine video duration.")
    except ffmpeg.Error as e:
        print(f"Error probing video: {e.stderr.decode('utf8')}")
        raise


def split_video(input_path, output_folder, chunk_duration_seconds):
    """Splits the video into chunks of specified duration."""
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")

    total_duration = get_video_duration(input_path)
    num_chunks = math.ceil(total_duration / chunk_duration_seconds)

    print(
        f"Video duration: {total_duration:.2f}s. Splitting into {num_chunks} chunks of {chunk_duration_seconds}s each."
    )

    for i in range(num_chunks):
        start_time = i * chunk_duration_seconds
        # For the last chunk, ensure it doesn't exceed total video duration
        current_chunk_duration = min(
            chunk_duration_seconds, total_duration - start_time
        )
        if current_chunk_duration <= 0:  # Should not happen if logic is correct
            continue

        output_filename = os.path.join(output_folder, f"chunk_{i+1:03d}.mp4")

        print(
            f"Processing chunk {i+1}/{num_chunks}: start={start_time:.2f}s, duration={current_chunk_duration:.2f}s -> {output_filename}"
        )

        try:
            (
                ffmpeg.input(input_path, ss=start_time, t=current_chunk_duration)
                .output(
                    output_filename, c="copy"
                )  # Use stream copy for speed if no re-encoding is needed
                .global_args("-loglevel", "error")  # Suppress verbose ffmpeg logs
                .run(overwrite_output=True)
            )
            print(f"[✓] Saved {output_filename}")
        except ffmpeg.Error as e:
            print(f"Error processing chunk {i+1}: {e.stderr.decode('utf8')}")
            # Attempt without stream copy if copy fails (e.g., format change or filter needed)
            try:
                print(f"Retrying chunk {i+1} without stream copy...")
                (
                    ffmpeg.input(input_path, ss=start_time, t=current_chunk_duration)
                    .output(output_filename)  # No c='copy'
                    .global_args("-loglevel", "error")
                    .run(overwrite_output=True)
                )
                print(f"[✓] Saved {output_filename} (after retry without stream copy)")
            except ffmpeg.Error as e_retry:
                print(
                    f"Error processing chunk {i+1} on retry: {e_retry.stderr.decode('utf8')}"
                )
                print(f"[✗] Failed to save {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a video file into N-second chunks."
    )
    parser.add_argument("--input", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--output_folder", required=True, help="Directory to save the video chunks."
    )
    parser.add_argument(
        "--duration", type=int, required=True, help="Duration of each chunk in seconds."
    )

    args = parser.parse_args()

    if args.duration <= 0:
        print("Error: Duration must be a positive integer.")
    else:
        split_video(args.input, args.output_folder, args.duration)
        print("Video splitting process completed.")
