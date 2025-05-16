import argparse
import os
from utils import load_clip_model, build_index, search_index


def main():
    parser = argparse.ArgumentParser(
        description="Search local media using CLIP and text queries."
    )
    parser.add_argument(
        "--media_folder",
        required=True,
        help="Path to the folder containing media files (images/videos).",
    )
    parser.add_argument("--query", required=True, help="Text query to search for.")
    parser.add_argument(
        "--top_k", type=int, default=5, help="Number of top results to return."
    )
    parser.add_argument(
        "--reindex", action="store_true", help="Force re-indexing of the media folder."
    )
    # Potentially add --output_json to save results to a file later

    args = parser.parse_args()

    if not os.path.isdir(args.media_folder):
        print(f"Error: Media folder not found at {args.media_folder}")
        return

    model, processor = (
        load_clip_model()
    )  # utils.MODEL_NAME can be changed there if needed

    index_data = build_index(args.media_folder, model, processor, args.reindex)

    if not index_data:
        print(
            "No media items were indexed. Ensure your media folder is not empty and contains supported file types."
        )
        return

    print(f"\nSearching for '{args.query}'...")
    results = search_index(args.query, index_data, model, processor, top_k=args.top_k)

    if results:
        print(f"\nFound {len(results)} result(s) for '{args.query}':")
        for i, (score, item) in enumerate(results):
            if item["type"] == "image":
                print(f"{i+1}. {item['path']} (Score: {score:.4f})")
            elif item["type"] == "video_frame":
                print(
                    f"{i+1}. {item['path']} (Frame at {item['timestamp']:.2f}s) (Score: {score:.4f})"
                )
    else:
        print(f"No results found for '{args.query}'.")


if __name__ == "__main__":
    main()
