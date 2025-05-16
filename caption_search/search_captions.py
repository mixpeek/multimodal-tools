import argparse
import os
import json
from utils import (
    extract_audio_from_video,
    transcribe_audio_file,
    load_transcript_from_file,
    search_segments,
    is_video_file,
    format_timestamp,
)


def main():
    parser = argparse.ArgumentParser(
        description="Search for text within video captions/transcript."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--video_input", help="Path to the input video file to transcribe and search."
    )
    group.add_argument(
        "--transcript_input",
        help="Path to an existing JSON transcript file (Whisper format).",
    )

    parser.add_argument(
        "--query", required=True, help="Text to search for in the captions."
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
        help="Whisper model size to use if --video_input is provided (default: base).",
    )
    parser.add_argument(
        "--output_transcript_file",
        help="Optional: Path to save the generated transcript if --video_input is used.",
    )

    args = parser.parse_args()

    transcript_data = None
    source_name = None  # To identify the origin of the transcript for display
    temp_audio_path = None

    try:
        if args.video_input:
            source_name = args.video_input
            if not os.path.exists(args.video_input):
                print(f"Error: Video input file not found at {args.video_input}")
                return
            if not is_video_file(args.video_input):
                # Technically Whisper can handle audio files directly, but our flow here is video-focused
                print(
                    f"Error: {args.video_input} does not appear to be a video file. Please provide a video or a transcript file."
                )
                return

            temp_audio_path = extract_audio_from_video(args.video_input)
            if not temp_audio_path:
                print(f"Could not extract audio from {args.video_input}")
                return

            print(
                f"Transcribing video {args.video_input} using model '{args.model_size}'..."
            )
            transcript_data = transcribe_audio_file(temp_audio_path, args.model_size)

            if args.output_transcript_file:
                try:
                    with open(args.output_transcript_file, "w", encoding="utf-8") as f:
                        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
                    print(
                        f"Generated transcript saved to {args.output_transcript_file}"
                    )
                except Exception as e_save:
                    print(
                        f"Warning: Could not save transcript to {args.output_transcript_file}: {e_save}"
                    )

        elif args.transcript_input:
            source_name = args.transcript_input
            if not os.path.exists(args.transcript_input):
                print(
                    f"Error: Transcript input file not found at {args.transcript_input}"
                )
                return
            transcript_data = load_transcript_from_file(args.transcript_input)

        if not transcript_data or "segments" not in transcript_data:
            print(
                f"Could not load or generate valid transcript from '{source_name or 'input'}'. Cannot perform search."
            )
            return

        print(f"\nSearching for query '{args.query}' in '{source_name}'...")
        found_items = search_segments(transcript_data["segments"], args.query)

        if found_items:
            print(f"\nFound query '{args.query}' in '{source_name}':")
            for item in found_items:
                start_time_str = format_timestamp(item["start"])
                end_time_str = format_timestamp(item["end"])
                print(
                    f"- Segment ({start_time_str} - {end_time_str}): \"{item['text'].strip()}\""
                )
        else:
            print(f"Query '{args.query}' not found in '{source_name}'.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            print(f"Cleaning up temporary audio file: {temp_audio_path}")
            os.remove(temp_audio_path)


if __name__ == "__main__":
    main()
