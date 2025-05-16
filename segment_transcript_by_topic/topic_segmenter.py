from sentence_transformers import SentenceTransformer
import numpy as np
import hdbscan


def segment_by_topic(segments):
    if not segments:
        return []

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [s["text"] for s in segments]
    embeddings = model.encode(texts)

    # Ensure embeddings are 2D for HDBSCAN
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(-1, 1)
    # HDBSCAN requires at least 2 samples if min_cluster_size is 2 or more.
    # if less samples than min_cluster_size, hdbscan might error or produce all -1 labels
    # We can set allow_single_cluster=True if we want to allow a single cluster in such cases.
    # For now, let's ensure min_cluster_size is not greater than number of samples.
    min_samples_for_hdbscan = 2
    current_min_cluster_size = 2

    if len(embeddings) < min_samples_for_hdbscan:
        # Not enough data to form clusters, return all segments as unclustered or a single topic
        # For simplicity, returning them as unclustered. Or assign all to topic 0.
        print(
            f"Warning: Not enough segments ({len(embeddings)}) for robust clustering with min_cluster_size={current_min_cluster_size}. Assigning all to topic 0 or handling as unclustered."
        )
        # Option 1: Treat all as one topic if too few segments
        # cluster_labels = np.zeros(len(embeddings), dtype=int)
        # Option 2: Or, more accurately, mark them as unclustered (noise) if that's preferred.
        # However, the original code filters out -1, so let's assign to topic 0 if too few.
        # Fallback: if even fewer than 1 meaningful segment after transcription, it's tricky.
        # The original code filters label == -1, so if all are -1, output is empty.
        # If we want at least one segment, we might need to adjust logic.
        # Let's try to assign them to a single cluster if very few.
        if len(embeddings) > 0:
            cluster_labels = np.zeros(len(embeddings), dtype=int)  # All to topic 0
        else:
            return []  # No segments to process
    else:
        adjusted_min_cluster_size = min(current_min_cluster_size, len(embeddings))
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=max(2, adjusted_min_cluster_size),
            metric="euclidean",
            allow_single_cluster=True,
        )
        cluster_labels = clusterer.fit_predict(embeddings)

    grouped = []
    for i, (label, seg) in enumerate(zip(cluster_labels, segments)):
        # Original code skips label == -1. If allow_single_cluster=True and few samples,
        # HDBSCAN might still produce -1 if it can't form a cluster.
        # If we assigned all to topic 0 above for very few segments, this check is fine.
        if label == -1:
            # Optionally, we could assign noise points to their own unique topic IDs
            # or a generic 'unclassified' topic ID if desired.
            # For now, sticking to original behavior of filtering them out.
            continue
        grouped.append(
            {
                "topic_id": int(label),
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
            }
        )

    # Sort by topic_id and then by start time
    grouped.sort(key=lambda x: (x["topic_id"], x["start"]))
    return grouped
