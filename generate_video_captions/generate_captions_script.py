import argparse
import os
from utils import (
    extract_audio_from_media,
    transcribe_to_segments,
    generate_srt_content,
    generate_vtt_content,
    is_video_file,  # Though the script will try to process any input with ffmpeg
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate SRT and VTT caption files from video or audio."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the input video or audio file."
    )
    parser.add_argument(
        "--output_dir",
        help="Optional: Directory to save the caption files. Defaults to input file's directory.",
    )
    parser.add_argument(
        "--model_size",
        default="base",
        choices=[
            "tiny",
            "base",
            "small",
            "medium",
            "large",
            "large-v1",
            "large-v2",
            "large-v3",
        ],
        help="Whisper model size to use (default: base).",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found at {args.input}")
        return

    output_directory = args.output_dir
    if not output_directory:
        output_directory = os.path.dirname(os.path.abspath(args.input))

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    base_filename = os.path.splitext(os.path.basename(args.input))[0]
    srt_path = os.path.join(output_directory, f"{base_filename}.srt")
    vtt_path = os.path.join(output_directory, f"{base_filename}.vtt")

    temp_audio_path = None
    try:
        # Note: extract_audio_from_media will attempt to convert any input to WAV for Whisper
        # This simplifies logic as Whisper works best with WAV.
        temp_audio_path = extract_audio_from_media(args.input)
        if not temp_audio_path:
            print(f"Could not prepare audio from {args.input}")
            return

        print(
            f"Generating transcript segments for {args.input} using model '{args.model_size}'..."
        )
        segments = transcribe_to_segments(temp_audio_path, args.model_size)

        if not segments:
            print("No segments transcribed. Cannot generate caption files.")
            return

        # Generate SRT content
        srt_content = generate_srt_content(segments)
        with open(srt_path, "w", encoding="utf-8") as f_srt:
            f_srt.write(srt_content)
        print(f"[✓] SRT captions saved to {srt_path}")

        # Generate VTT content
        vtt_content = generate_vtt_content(segments)
        with open(vtt_path, "w", encoding="utf-8") as f_vtt:
            f_vtt.write(vtt_content)
        print(f"[✓] WebVTT captions saved to {vtt_path}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            print(f"Cleaning up temporary audio file: {temp_audio_path}")
            os.remove(temp_audio_path)


if __name__ == "__main__":
    main()
