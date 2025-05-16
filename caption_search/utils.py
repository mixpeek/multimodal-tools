import os
import whisper
import ffmpeg
import tempfile
import json


def is_video_file(filepath):
    """Checks if the filepath is likely a video file based on extension."""
    video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"]
    return os.path.splitext(filepath)[1].lower() in video_extensions


def extract_audio_from_video(video_path):
    """Extracts audio from a video file and saves it as a temporary WAV file."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        output_audio_path = tmpfile.name

    print(f"Extracting audio from {video_path} to {output_audio_path}...")
    try:
        (
            ffmpeg.input(video_path)
            .output(
                output_audio_path, acodec="pcm_s16le", ar="16000", ac=1
            )  # Standard format for Whisper
            .global_args("-loglevel", "error")
            .run(overwrite_output=True)
        )
        print("Audio extraction successful.")
        return output_audio_path
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode('utf8')}")
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
        raise
    except Exception as e_gen:
        print(f"A general error occurred during audio extraction: {str(e_gen)}")
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
        raise


def transcribe_audio_file(audio_path, model_size="base"):
    """Transcribes an audio file using OpenAI Whisper and returns the full result object."""
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    print(f"Transcribing {audio_path}...")
    # We need segments with timestamps
    result = model.transcribe(
        audio_path, verbose=False
    )  # verbose=False to keep console cleaner by default
    print("Transcription complete.")
    return result  # Return the full result which includes the segments list


def load_transcript_from_file(transcript_path):
    """Loads a transcript from a JSON file (expected Whisper format)."""
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_data = json.load(f)
        if "segments" not in transcript_data:
            raise ValueError("Transcript file does not contain 'segments' key.")
        return transcript_data
    except FileNotFoundError:
        print(f"Error: Transcript file not found at {transcript_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from transcript file: {transcript_path}")
        return None
    except Exception as e:
        print(f"Error loading transcript file {transcript_path}: {e}")
        return None


def search_segments(segments, query_text):
    """Searches for query_text (case-insensitive) within transcript segments."""
    found_segments = []
    if not segments:
        return found_segments

    query_lower = query_text.lower()
    for segment in segments:
        if "text" in segment and query_lower in segment["text"].lower():
            found_segments.append(segment)
    return found_segments


def format_timestamp(seconds):
    """Formats seconds into a human-readable MmSs string (e.g., 02m30s)."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}m{secs:02d}s"
