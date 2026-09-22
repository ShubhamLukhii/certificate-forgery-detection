from pathlib import Path

import pandas as pd


# Root directory of the downloaded dataset.
DATASET_DIR = Path("data/cache/RealText-V2")

# Directory for generated/processed metadata.
OUTPUT_DIR = Path("data/processed")

# Final prepared metadata file.
OUTPUT_FILE = OUTPUT_DIR / "training_metadata.csv"


# Supported image and mask file extensions.
SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


def build_file_index(directory):
    """
    Recursively index image or mask files inside a directory.

    The filename is used as the dictionary key and the complete
    local path is stored as the value.

    Raises:
        ValueError: If duplicate filenames are found.
    """

    file_index = {}

    if not directory.exists():
        raise FileNotFoundError(
            f"Directory not found: {directory}"
        )

    for file_path in directory.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        filename = file_path.name

        # A duplicate filename could cause a metadata record
        # to be matched with the wrong physical file.
        if filename in file_index:
            raise ValueError(
                f"Duplicate filename found: {filename}\n"
                f"Existing path: {file_index[filename]}\n"
                f"Duplicate path: {file_path}"
            )

        file_index[filename] = file_path

    return file_index


def validate_authenticity_labels(metadata):
    """
    Validate and convert the dataset authenticity labels.

    white -> 0 (pristine)
    black -> 1 (forged)
    """

    expected_types = {"white", "black"}

    actual_types = set(
        metadata["type"].dropna().unique()
    )

    unknown_types = actual_types - expected_types

    if unknown_types:
        raise ValueError(
            "Validation failed: unknown authenticity labels found: "
            f"{sorted(unknown_types)}"
        )

    metadata["label"] = metadata["type"].map(
        {
            "white": 0,
            "black": 1,
        }
    )

    # Every record must have a valid numerical label.
    missing_labels = metadata["label"].isna()

    if missing_labels.any():
        raise ValueError(
            "Validation failed: "
            f"{missing_labels.sum()} records have no valid label."
        )

    return metadata


def validate_image_paths(metadata):
    """
    Validate that every metadata record has a matching image file.
    """

    missing_images = metadata["image_path"].isna()

    if missing_images.any():
        missing_count = missing_images.sum()

        missing_files = metadata.loc[
            missing_images,
            "image_file",
        ].head(10).tolist()

        raise ValueError(
            f"Validation failed: {missing_count} required image files "
            "could not be found.\n"
            f"Examples: {missing_files}"
        )


def validate_forged_masks(metadata):
    """
    Validate that every forged sample has a valid mask.

    Forged samples are represented by label = 1.
    """

    forged_samples = metadata["label"] == 1

    missing_forged_masks = (
        forged_samples
        & metadata["mask_path"].isna()
    )

    if missing_forged_masks.any():
        missing_count = missing_forged_masks.sum()

        missing_files = metadata.loc[
            missing_forged_masks,
            "mask_file",
        ].head(10).tolist()

        raise ValueError(
            "Validation failed: "
            f"{missing_count} forged samples are missing required "
            f"masks.\nExamples: {missing_files}"
        )


def main():
    """
    Prepare and validate training metadata from the local dataset.

    The original cached dataset is read only. No files inside
    data/cache/RealText-V2 are modified by this script.
    """

    # ------------------------------------------------------------------
    # Check metadata file
    # ------------------------------------------------------------------

    metadata_path = DATASET_DIR / "metadata.parquet"

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {metadata_path}"
        )

    print("Loading dataset metadata...")

    metadata = pd.read_parquet(metadata_path)

    print(f"Loaded {len(metadata)} metadata records.")

    # ------------------------------------------------------------------
    # Check required metadata columns
    # ------------------------------------------------------------------

    required_columns = {
        "sample_id",
        "language",
        "language_code",
        "type",
        "image_file",
        "mask_file",
        "has_mask",
        "report_file",
        "report_text",
    }

    missing_columns = (
        required_columns - set(metadata.columns)
    )

    if missing_columns:
        raise ValueError(
            "Validation failed: required metadata columns are missing: "
            f"{sorted(missing_columns)}"
        )

    # ------------------------------------------------------------------
    # Index image files
    # ------------------------------------------------------------------

    print("\nIndexing image files...")

    image_index = {}

    for split in ("train", "test"):
        image_directory = DATASET_DIR / split / "image"

        split_index = build_file_index(
            image_directory
        )

        image_index.update(split_index)

    print(
        f"Indexed {len(image_index)} image files."
    )

    # ------------------------------------------------------------------
    # Index mask files
    # ------------------------------------------------------------------

    print("\nIndexing mask files...")

    mask_index = build_file_index(
    DATASET_DIR / "train" / "mask"
)

    print(
    f"Indexed {len(mask_index)} mask files."
)

    # ------------------------------------------------------------------
    # Match metadata filenames to local image files
    # ------------------------------------------------------------------

    metadata["image_path"] = metadata["image_file"].map(
        lambda filename: (
            str(image_index[filename])
            if pd.notna(filename)
            and filename in image_index
            else None
        )
    )

    # ------------------------------------------------------------------
    # Match metadata filenames to local mask files
    # ------------------------------------------------------------------

    metadata["mask_path"] = metadata["mask_file"].map(
        lambda filename: (
            str(mask_index[filename])
            if pd.notna(filename)
            and filename in mask_index
            else None
        )
    )

    metadata["mask_exists"] = (
        metadata["mask_path"].notna()
    )

    # ------------------------------------------------------------------
    # Convert authenticity labels
    # ------------------------------------------------------------------

    metadata = validate_authenticity_labels(
        metadata
    )

    # ------------------------------------------------------------------
    # Validate image paths
    # ------------------------------------------------------------------

    validate_image_paths(metadata)

    # ------------------------------------------------------------------
    # Validate forged sample masks
    # ------------------------------------------------------------------

    validate_forged_masks(metadata)

    # ------------------------------------------------------------------
    # Select metadata required by downstream processing
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

    # ------------------------------------------------------------------
    # Print final dataset statistics
    # ------------------------------------------------------------------

    print("\nValidation successful.")

    print(
        f"Processed records: "
        f"{len(prepared_metadata)}"
    )

    print(
        f"Missing image paths: "
        f"{prepared_metadata['image_path'].isna().sum()}"
    )

    missing_forged_masks = (
        prepared_metadata["label"].eq(1)
        & prepared_metadata["mask_path"].isna()
    )

    print(
        "Missing forged-sample masks: "
        f"{missing_forged_masks.sum()}"
    )

    print("\nLabel distribution:")

    print(
        prepared_metadata["label"]
        .value_counts()
        .sort_index()
    )

    print("\nAuthenticity distribution:")

    print(
        prepared_metadata["type"]
        .value_counts()
    )

    print("\nMask availability:")

    print(
        prepared_metadata["mask_exists"]
        .value_counts()
    )

    print("\nLanguage distribution:")

    print(
        prepared_metadata["language"]
        .value_counts()
    )

    print("\nPrepared metadata shape:")

    print(
        prepared_metadata.shape
    )

    print("\nPrepared metadata saved to:")

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()