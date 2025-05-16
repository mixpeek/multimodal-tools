import os
import whisper
import ffmpeg
from pydub import (
    AudioSegment,
)  # Though not strictly used if ffmpeg handles conversion for whisper
import tempfile


def is_video_file(filepath):
    """Checks if the filepath is likely a video file based on extension."""
    video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"]
    return os.path.splitext(filepath)[1].lower() in video_extensions


def extract_audio_from_video(video_path):
    """Extracts audio from a video file and saves it as a temporary WAV file."""

    # Create a temporary file with a .wav extension
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        output_audio_path = tmpfile.name

    print(f"Extracting audio from {video_path} to {output_audio_path}...")
    try:
        (
            ffmpeg.input(video_path)
            .output(output_audio_path, acodec="pcm_s16le", ar="16000", ac=1)
            .global_args("-loglevel", "error")
            .run(overwrite_output=True)
        )
        print("Audio extraction successful.")
        return output_audio_path
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode('utf8')}")
        # Clean up temp file if extraction fails
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
        raise


def transcribe_audio_file(audio_path, model_size="base"):
    """Transcribes an audio file using OpenAI Whisper."""
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path)
    print("Transcription complete.")
    return result
