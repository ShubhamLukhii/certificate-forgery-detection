from pathlib import Path

from huggingface_hub import snapshot_download


# Hugging Face dataset repository
DATASET_REPO = "vankey/RealText-V2"

# Local directory for the complete dataset
DATASET_DIR = Path("data/cache/RealText-V2")


def download_dataset():
    """
    Download the complete RealText-V2 dataset repository.

    The downloaded files remain local and are ignored by Git.
    Anyone who clones the repository can run this script again.
    """

    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading RealText-V2 dataset...")
    print(f"Destination: {DATASET_DIR.resolve()}")

    local_path = snapshot_download(
        repo_id=DATASET_REPO,
        repo_type="dataset",
        local_dir=str(DATASET_DIR)
    )

    print("\nDataset download completed.")
    print(f"Dataset location: {local_path}")

    metadata_path = DATASET_DIR / "metadata.parquet"

    if metadata_path.exists():
        print(f"Metadata found at: {metadata_path}")
    else:
        print("Warning: metadata.parquet was not found.")


if __name__ == "__main__":
    download_dataset()