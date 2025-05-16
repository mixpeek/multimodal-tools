import json
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

DEFAULT_MODEL_NAME = "facebook/bart-large-cnn"


def load_transcript_text(file_path):
    """Loads text from a .txt or Whisper .json transcript file."""
    if not file_path.lower().endswith((".txt", ".json")):
        raise ValueError("Input file must be a .txt or .json file.")

    try:
        if file_path.lower().endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Check for Whisper's full text field first
            if "text" in data and isinstance(data["text"], str):
                return data["text"]
            # Fallback to joining segments if full text field is not present
            elif "segments" in data and isinstance(data["segments"], list):
                full_text = " ".join(
                    [
                        segment["text"].strip()
                        for segment in data["segments"]
                        if "text" in segment and isinstance(segment["text"], str)
                    ]
                )
                if full_text:
                    return full_text
                else:
                    raise ValueError(
                        "JSON file seems to be a Whisper transcript but contains no usable text in segments."
                    )
            else:
                raise ValueError(
                    "JSON file does not conform to expected Whisper transcript format (missing 'text' or 'segments' key)."
                )
        else:  # .txt file
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except FileNotFoundError:
        print(f"Error: Transcript file not found at {file_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        raise
    except Exception as e:
        print(f"Error loading transcript from {file_path}: {e}")
        raise


def summarize_text(
    text_to_summarize, model_name=None, min_length=30, max_length=150, device=None
):
    """Summarizes the given text using a Hugging Face Transformers model."""
    if not text_to_summarize.strip():
        print(
            "Warning: Input text is empty or contains only whitespace. Returning empty summary."
        )
        return ""

    active_model_name = model_name if model_name else DEFAULT_MODEL_NAME

    if device is None:
        device = (
            0 if torch.cuda.is_available() else -1
        )  # Use GPU if available, otherwise CPU

    print(
        f"Loading summarization model: {active_model_name} (device: {'gpu' if device == 0 else 'cpu'})..."
    )

    try:
        # Using pipeline for easier handling
        summarizer = pipeline(
            "summarization",
            model=active_model_name,
            tokenizer=active_model_name,
            device=device,
        )
        print(
            f"Summarizing text (min_length={min_length}, max_length={max_length})... This may take a while for long texts."
        )

        # Handle potential token limits of the model. Some models have strict input length limits.
        # A common approach is to chunk, but for a single summary, we might truncate or rely on the model's handling.
        # For simplicity here, we pass the whole text. More robust solutions might chunk and summarize iteratively.
        # The `transformers` pipeline often handles truncation by default based on model config, but it's good to be aware.

        summary_list = summarizer(
            text_to_summarize,
            min_length=min_length,
            max_length=max_length,
            truncation=True,
        )
        if (
            summary_list
            and isinstance(summary_list, list)
            and "summary_text" in summary_list[0]
        ):
            summary = summary_list[0]["summary_text"]
            print("Summarization complete.")
            return summary
        else:
            print(
                "Error: Summarization pipeline did not return expected output format."
            )
            return ""

    except Exception as e:
        print(f"Error during summarization with model {active_model_name}: {e}")
        # Fallback or more specific error handling could be added here
        # For example, if model loading fails, could try a different default model
        if "sentencepiece" in str(e).lower() and "not installed" in str(e).lower():
            print(
                "Hint: The selected model might require 'sentencepiece'. Try: pip install sentencepiece"
            )
        if (
            "Token indices sequence length is longer than the specified maximum sequence length"
            in str(e)
        ):
            print(
                f"Hint: The input text is too long for the model '{active_model_name}'. Consider a model with a larger context window or implement input chunking."
            )
        raise
