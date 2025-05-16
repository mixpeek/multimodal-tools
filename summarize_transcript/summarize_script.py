import argparse
import os
from utils import load_transcript_text, summarize_text

DEFAULT_MIN_LENGTH = 30
DEFAULT_MAX_LENGTH = 150
# Common summarization models:
# "facebook/bart-large-cnn"
# "t5-small", "t5-base", "t5-large"
# "google/pegasus-xsum"
DEFAULT_MODEL = "facebook/bart-large-cnn"


def main():
    parser = argparse.ArgumentParser(
        description="Summarize a transcript from a .txt or Whisper .json file."
    )
    parser.add_argument(
        "--input_file",
        required=True,
        help="Path to the input transcript file (.txt or .json).",
    )
    parser.add_argument(
        "--output_file",
        required=True,
        help="Path to save the generated summary (.txt).",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Name of the Hugging Face summarization model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--min_length",
        type=int,
        default=DEFAULT_MIN_LENGTH,
        help=f"Minimum length of the summary in tokens (default: {DEFAULT_MIN_LENGTH}).",
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=DEFAULT_MAX_LENGTH,
        help=f"Maximum length of the summary in tokens (default: {DEFAULT_MAX_LENGTH}).",
    )
    # Add device argument if specific GPU/CPU control is needed beyond default
    # parser.add_argument("--device", type=str, default=None, help="Device to use: 'cuda', 'cpu', or None for auto-detect.")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found at {args.input_file}")
        return

    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    try:
        print(f"Loading transcript from: {args.input_file}")
        transcript_text = load_transcript_text(args.input_file)

        if not transcript_text or not transcript_text.strip():
            print("Transcript is empty. Cannot generate summary.")
            # Optionally write an empty file or a note
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(
                    "[No summary generated: Input transcript was empty or invalid.]"
                )
            return

        summary = summarize_text(
            transcript_text,
            model_name=args.model_name,
            min_length=args.min_length,
            max_length=args.max_length,
            # device=args.device # Pass if device arg is added
        )

        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"[✓] Summary successfully saved to {args.output_file}")

    except ValueError as ve:
        print(f"A value error occurred: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
