import os
import whisper
import ffmpeg
import tempfile
import datetime


def is_video_file(filepath):
    """Checks if the filepath is likely a video file based on extension."""
    video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"]
    # Add more audio extensions if Whisper is to handle them directly without ffmpeg pre-conversion
    # audio_extensions = ['.mp3', '.wav', '.m4a', '.ogg']
    ext = os.path.splitext(filepath)[1].lower()
    return ext in video_extensions


def extract_audio_from_media(media_path):
    """Extracts audio from a video/audio file and saves it as a temporary WAV file if necessary."""
    # Whisper can handle many audio formats directly. We primarily need to extract from video.
    # If it's already an audio file that Whisper supports, we might not need to convert.
    # However, for simplicity and consistency, converting to WAV is a safe bet.

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        output_audio_path = tmpfile.name

    print(f"Preparing audio from {media_path} to {output_audio_path}...")
    try:
        (
            ffmpeg.input(media_path)
            .output(
                output_audio_path, acodec="pcm_s16le", ar="16000", ac=1
            )  # Standard for Whisper
            .global_args("-loglevel", "error")
            .run(overwrite_output=True)
        )
        print("Audio preparation successful.")
        return output_audio_path
    except ffmpeg.Error as e:
        print(f"Error preparing audio: {e.stderr.decode('utf8')}")
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
        raise
    except Exception as e_gen:
        print(f"A general error occurred during audio preparation: {str(e_gen)}")
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
        raise


def transcribe_to_segments(audio_path, model_size="base"):
    """Transcribes an audio file and returns the segments list from Whisper."""
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path, verbose=False)
    print("Transcription complete.")
    return result.get("segments", [])


def format_time_srt(seconds):
    """Formats seconds to SRT time format: HH:MM:SS,mmm"""
    delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def format_time_vtt(seconds):
    """Formats seconds to WebVTT time format: HH:MM:SS.mmm or MM:SS.mmm"""
    delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    else:
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def generate_srt_content(segments):
    """Generates SRT formatted caption string from Whisper segments."""
    srt_content = []
    for i, segment in enumerate(segments):
        start_time = format_time_srt(segment["start"])
        end_time = format_time_srt(segment["end"])
        text = segment["text"].strip()
        srt_content.append(f"{i+1}\n{start_time} --> {end_time}\n{text}\n")
    return "\n".join(srt_content)


def generate_vtt_content(segments):
    """Generates WebVTT formatted caption string from Whisper segments."""
    vtt_content = ["WEBVTT\n"]
    for segment in segments:
        start_time = format_time_vtt(segment["start"])
        end_time = format_time_vtt(segment["end"])
        text = segment["text"].strip()
        vtt_content.append(f"{start_time} --> {end_time}\n{text}\n")
    return "\n".join(vtt_content)
