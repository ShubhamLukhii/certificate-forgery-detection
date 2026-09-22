from pathlib import Path

import pandas as pd


# Root directory of the downloaded dataset
DATASET_DIR = Path("data/cache/RealText-V2")

# Output directory for prepared metadata
OUTPUT_DIR = Path("data/processed")

# Output metadata file
OUTPUT_FILE = OUTPUT_DIR / "training_metadata.csv"


def build_file_index(directory):
    """
    Recursively find image files inside a directory.

    Returns:
        dict: filename -> full local file path
    """

    file_index = {}

    supported_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }

    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            filename = file_path.name

            if filename in file_index:
                raise ValueError(
                    f"Duplicate filename found: {filename}\n"
                    f"Existing path: {file_index[filename]}\n"
                    f"Duplicate path: {file_path}"
                )

            file_index[filename] = file_path

    return file_index


def main():
    """
    Prepare a clean metadata manifest for model development.
    """

    metadata_path = DATASET_DIR / "metadata.parquet"

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {metadata_path}"
        )

    print("Loading dataset metadata...")

    metadata = pd.read_parquet(metadata_path)

    print(f"Loaded {len(metadata)} metadata records.")

    # ------------------------------------------------------------------
    # Build image and mask indexes
    # ------------------------------------------------------------------

    print("\nIndexing image files...")

    image_index = build_file_index(
        DATASET_DIR / "train" / "image"
    )

    image_index.update(
        build_file_index(
            DATASET_DIR / "test" / "image"
        )
    )

    print(f"Indexed {len(image_index)} image files.")

    print("\nIndexing mask files...")

    mask_index = build_file_index(
        DATASET_DIR / "train" / "mask"
    )

    mask_index.update(
        build_file_index(
            DATASET_DIR / "test" / "mask"
        )
    )

    print(f"Indexed {len(mask_index)} mask files.")

    # ------------------------------------------------------------------
    # Map metadata filenames to local paths
    # ------------------------------------------------------------------

    metadata["image_path"] = metadata["image_file"].map(
        lambda filename: str(image_index.get(filename))
        if pd.notna(filename)
        else None
    )

    metadata["mask_path"] = metadata["mask_file"].map(
        lambda filename: str(mask_index.get(filename))
        if pd.notna(filename)
        else None
    )

    # ------------------------------------------------------------------
    # Convert authenticity labels
    # ------------------------------------------------------------------

    # white = pristine
    # black = forged
    label_mapping = {
        "white": 0,
        "black": 1,
    }

    metadata["label"] = metadata["type"].map(label_mapping)

    # ------------------------------------------------------------------
    # Validate image paths
    # ------------------------------------------------------------------

    missing_images = metadata["image_path"].isna()

    if missing_images.any():
        missing_count = missing_images.sum()

        print(
            f"\nWARNING: {missing_count} metadata records "
            "do not have matching image files."
        )

    # ------------------------------------------------------------------
    # Validate mask paths
    # ------------------------------------------------------------------

    metadata["mask_exists"] = metadata["mask_path"].notna()

    # ------------------------------------------------------------------
    # Keep the columns required for downstream processing
    # ------------------------------------------------------------------

    prepared_metadata = metadata[
        [
            "sample_id",
            "language",
            "language_code",
            "type",
            "label",
            "image_file",
            "image_path",
            "mask_file",
            "mask_path",
            "mask_exists",
            "has_mask",
            "report_file",
            "report_text",
        ]
    ].copy()

    # ------------------------------------------------------------------
    # Create output directory
    # ------------------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------------------
    # Save prepared metadata
    # ------------------------------------------------------------------

    prepared_metadata.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\nPrepared metadata saved to:")
    print(OUTPUT_FILE)

    print("\nPrepared metadata shape:")
    print(prepared_metadata.shape)

    print("\nLabel distribution:")
    print(prepared_metadata["label"].value_counts(dropna=False))

    print("\nMissing image paths:")
    print(
        prepared_metadata["image_path"]
        .isna()
        .sum()
    )

    print("\nMask availability:")
    print(
        prepared_metadata["mask_exists"]
        .value_counts(dropna=False)
    )


if __name__ == "__main__":
    main()