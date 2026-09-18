from pathlib import Path

import pandas as pd


# Root directory of the downloaded dataset
DATASET_DIR = Path("data/cache/RealText-V2")


def main():
    """
    Inspect metadata from the locally downloaded dataset.
    """

    metadata_path = DATASET_DIR / "metadata.parquet"

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {metadata_path}"
        )

    # Read the local metadata file.
    metadata = pd.read_parquet(metadata_path)

    print("Metadata shape:")
    print(metadata.shape)

    print("\nMetadata columns:")
    print(metadata.columns.tolist())

    print("\nFirst five records:")
    print(metadata.head())

    print("\nData types:")
    print(metadata.dtypes)

    print("\nAuthenticity distribution:")
    print(metadata["type"].value_counts(dropna=False))

    print("\nMask availability:")
    print(metadata["has_mask"].value_counts(dropna=False))

    print("\nLanguage distribution:")
    print(metadata["language"].value_counts(dropna=False))

    print("\nExample image paths:")
    print(
        metadata["image_file"]
        .head(10)
        .to_string(index=False)
    )

    print("\nExample mask paths:")
    print(
        metadata["mask_file"]
        .dropna()
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()