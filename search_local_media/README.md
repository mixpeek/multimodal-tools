# 📸 Search Local Media with Text (CLIP)

This Python tool uses OpenAI's CLIP model to perform text-based searches across a local folder of images and videos. It finds media files that best match your textual description.

### 🔧 Features
-   Indexes images (JPEG, PNG) and videos (extracts frames from MP4, AVI, MOV, etc.).
-   Uses a pre-trained CLIP model for generating image and text embeddings.
-   Calculates cosine similarity to find the best matches for your text query.
-   Caches media embeddings for faster subsequent searches.
-   Option to specify which CLIP model to use.

### 🏁 Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Create an example media folder
mkdir -p examples/my_media/
# (Add some .jpg, .png, .mp4 files into examples/my_media/)

# Run a search
python search_script.py --media_folder examples/my_media/ --query "a picture of a cat playing"

# To see more options
python search_script.py --help
```

### ⚙️ How it Works
1.  **Indexing**: When run for the first time on a media folder (or if `--reindex` is used), the tool scans for image and video files.
    *   For images, it generates and stores CLIP embeddings.
    *   For videos, it extracts a few representative frames, then generates and stores embeddings for these frames.
    *   Embeddings are saved in an `index.pkl` file within the media folder to speed up future searches.
2.  **Searching**: 
    *   The tool loads the pre-computed media embeddings (or generates them if no index exists).
    *   It converts your text query into a CLIP embedding.
    *   It then compares the query embedding with all media embeddings using cosine similarity and returns the top matches.

### 📂 Output
The script will print a list of matched media files (and specific frame times for videos) along with their similarity scores.

```
Found 3 results for 'a picture of a cat playing':
1. examples/my_media/cat_on_sofa.jpg (Score: 0.85)
2. examples/my_media/funny_pets.mp4 (Frame at 10.5s) (Score: 0.78)
3. examples/my_media/kitten.png (Score: 0.75)
``` 