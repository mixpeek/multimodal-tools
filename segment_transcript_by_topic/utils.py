import os
import whisper
import ffmpeg
from pydub import AudioSegment


def extract_audio(input_path):
    output_path = "temp_audio.wav"
    # Ensure the command runs silently and overwrites output without confirmation
    try:
        (
            ffmpeg.input(input_path)
            .output(
                output_path, acodec="pcm_s16le", ar="16000", ac=1
            )  # Specify audio codec and sample rate for WAV
            .global_args("-loglevel", "error")  # Suppress ffmpeg logs except errors
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        print("stdout:", e.stdout.decode("utf8"))
        print("stderr:", e.stderr.decode("utf8"))
        raise e
    return output_path


def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    # Clean up the temporary audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)
    return result["segments"]
