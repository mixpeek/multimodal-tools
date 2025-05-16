import argparse
from utils import extract_audio, transcribe_audio
from topic_segmenter import segment_by_topic

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="segments.json")
    args = parser.parse_args()

    audio_path = extract_audio(args.input)
    transcript = transcribe_audio(audio_path)

    segments = segment_by_topic(transcript)

    import json

    with open(args.output, "w") as f:
        json.dump(segments, f, indent=2)

    print(f"[✓] Segmented transcript saved to {args.output}")
