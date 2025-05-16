import argparse
import json
import os
from utils import extract_audio_from_video, transcribe_audio_file, is_video_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe an audio or video file using OpenAI Whisper."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the input audio or video file."
    )
    parser.add_argument(
        "--output",
        default="transcript.json",
        help="Path to save the output JSON transcription.",
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
        exit(1)

    temp_audio_path = None
    input_for_transcription = args.input

    try:
        if is_video_file(args.input):
            print(f"Input file {args.input} appears to be a video. Extracting audio...")
            temp_audio_path = extract_audio_from_video(args.input)
            input_for_transcription = temp_audio_path
        else:
            print(f"Input file {args.input} appears to be an audio file.")

        if not input_for_transcription:
            print(f"Error: Could not prepare audio for transcription from {args.input}")
            exit(1)

        transcript_result = transcribe_audio_file(
            input_for_transcription, args.model_size
        )

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(transcript_result, f, indent=2, ensure_ascii=False)

        print(f"[✓] Transcription saved to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            print(f"Cleaning up temporary audio file: {temp_audio_path}")
            os.remove(temp_audio_path)
