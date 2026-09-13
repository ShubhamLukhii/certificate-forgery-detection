from huggingface_hub import hf_hub_download
import pandas as pd


DATASET_REPO = "vankey/RealText-V2"


def main():
    # Download only the metadata file.
    # This should be much smaller than downloading the complete dataset.
    metadata_path = hf_hub_download(
        repo_id=DATASET_REPO,
        filename="metadata.parquet",
        repo_type="dataset",
    )

    print("Metadata file downloaded to:")
    print(metadata_path)

    # Read the metadata file.
    metadata = pd.read_parquet(metadata_path)

    print("\nMetadata shape:")
    print(metadata.shape)

    print("\nMetadata columns:")
    print(metadata.columns.tolist())

    print("\nFirst five records:")
    print(metadata.head())

    print("\nData types:")
    print(metadata.dtypes)

    # Display the distribution of the authenticity field.
    if "type" in metadata.columns:
        print("\nValues in 'type':")
        print(metadata["type"].value_counts(dropna=False))

    # Display whether masks are available.
    if "has_mask" in metadata.columns:
        print("\nValues in 'has_mask':")
        print(metadata["has_mask"].value_counts(dropna=False))

    # Display language distribution.
    if "language" in metadata.columns:
        print("\nLanguage distribution:")
        print(metadata["language"].value_counts(dropna=False))

    # Display a few forged samples.
    if "type" in metadata.columns:
        forged_samples = metadata[metadata["type"] == "black"]

        print("\nNumber of forged samples:")
        print(len(forged_samples))

        print("\nFirst forged samples:")
        print(forged_samples.head())

    # Display a few pristine samples.
    if "type" in metadata.columns:
        pristine_samples = metadata[metadata["type"] == "white"]

        print("\nNumber of pristine samples:")
        print(len(pristine_samples))

        print("\nFirst pristine samples:")
        print(pristine_samples.head())


if __name__ == "__main__":
    main()