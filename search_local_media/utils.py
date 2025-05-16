import os
import pickle
import ffmpeg
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from tqdm import tqdm
import io

MODEL_NAME = "openai/clip-vit-base-patch32"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"]
FRAMES_PER_VIDEO = 5  # Number of frames to extract per video


# --- Model Loading ---
def load_clip_model():
    print(f"Loading CLIP model '{MODEL_NAME}' on {DEVICE}...")
    model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    print("CLIP model loaded.")
    return model, processor


# --- Embedding Generation ---
def get_text_embedding(text, model, processor):
    inputs = processor(
        text=text, return_tensors="pt", padding=True, truncation=True
    ).to(DEVICE)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    return text_features.cpu().numpy()


def get_image_embedding(image_pil, model, processor):
    if image_pil.mode != "RGB":
        image_pil = image_pil.convert("RGB")
    inputs = processor(images=image_pil, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    return image_features.cpu().numpy()


# --- Media Processing ---
def extract_frames_from_video(video_path, num_frames=FRAMES_PER_VIDEO):
    """Extracts specified number of frames evenly spaced throughout the video."""
    extracted_frames = []
    try:
        probe = ffmpeg.probe(video_path)
        duration_str = next(
            (s["duration"] for s in probe["streams"] if s["codec_type"] == "video"),
            None,
        )
        if not duration_str:
            print(
                f"Warning: Could not get duration for {video_path}. Skipping frame extraction."
            )
            return []
        duration = float(duration_str)
        if duration == 0:
            return []

        interval = duration / (num_frames + 1)
        for i in range(1, num_frames + 1):
            timestamp = interval * i
            out, _ = (
                ffmpeg.input(video_path, ss=timestamp)
                .output(
                    "pipe:", vframes=1, format="image2pipe", vcodec="png"
                )  # Output to pipe as png
                .global_args("-loglevel", "error")
                .run(capture_stdout=True, capture_stderr=True)
            )
            if out:
                image = Image.open(io.BytesIO(out)).convert("RGB")
                extracted_frames.append(
                    {"image": image, "timestamp": timestamp, "source_video": video_path}
                )
    except ffmpeg.Error as e:
        print(
            f"Error extracting frames from {video_path}: {e.stderr.decode('utf8') if e.stderr else 'Unknown ffmpeg error'}"
        )
    except Exception as e:
        print(f"General error extracting frames from {video_path}: {str(e)}")
    return extracted_frames


def discover_media_files(folder_path):
    media_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
                media_files.append(os.path.join(root, file))
    return media_files


# --- Indexing ---
def build_index(media_folder, model, processor, reindex=False):
    index_path = os.path.join(media_folder, "clip_media_index.pkl")
    if not reindex and os.path.exists(index_path):
        print(f"Loading existing index from {index_path}")
        with open(index_path, "rb") as f:
            return pickle.load(f)

    print(f"Building new index for {media_folder}...")
    media_files = discover_media_files(media_folder)
    index_data = (
        []
    )  # List of dicts: {'path': str, 'type': 'image'/'video_frame', 'timestamp': float_or_None, 'embedding': np.array}

    for media_path in tqdm(media_files, desc="Indexing media"):
        ext = os.path.splitext(media_path)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            try:
                img = Image.open(media_path)
                embedding = get_image_embedding(img, model, processor)
                index_data.append(
                    {
                        "path": media_path,
                        "type": "image",
                        "timestamp": None,
                        "embedding": embedding[0],
                    }
                )
            except Exception as e:
                print(f"Error processing image {media_path}: {e}")
        elif ext in VIDEO_EXTENSIONS:
            frames_data = extract_frames_from_video(
                media_path, num_frames=FRAMES_PER_VIDEO
            )
            for frame_info in frames_data:
                try:
                    embedding = get_image_embedding(
                        frame_info["image"], model, processor
                    )
                    index_data.append(
                        {
                            "path": media_path,
                            "type": "video_frame",
                            "timestamp": frame_info["timestamp"],
                            "embedding": embedding[0],
                        }
                    )
                except Exception as e:
                    print(
                        f"Error processing frame from {media_path} at {frame_info['timestamp']:.2f}s: {e}"
                    )

    with open(index_path, "wb") as f:
        pickle.dump(index_data, f)
    print(f"Index built and saved to {index_path}")
    return index_data


# --- Searching ---
def search_index(query_text, index_data, model, processor, top_k=5):
    query_embedding = get_text_embedding(query_text, model, processor)

    similarities = []
    for item in index_data:
        sim = np.dot(query_embedding, item["embedding"]) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(item["embedding"])
        )
        similarities.append((sim[0], item))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return similarities[:top_k]
