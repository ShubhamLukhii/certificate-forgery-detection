from datasets import load_dataset


DATASET_NAME = "vankey/RealText-V2"


def main():
    # Load the dataset in streaming mode so the complete dataset
    # is not downloaded during inspection.
    dataset = load_dataset(
        DATASET_NAME,
        streaming=True,
    )

    print("Dataset structure:")
    print(dataset)

    print("\nAvailable splits:")
    print(dataset.keys())

    # Inspect each split.
    for split_name, split_data in dataset.items():
        print(f"\n--- Split: {split_name} ---")

        print("Dataset features:")
        print(split_data.features)

        # Read only the first sample.
        first_sample = next(iter(split_data))

        print("\nFirst sample keys:")
        print(first_sample.keys())

        print("\nImage information:")
        image = first_sample["image"]
        print("Image type:", type(image))
        print("Image mode:", image.mode)
        print("Image size:", image.size)

        print("\nLabel information:")
        print("Label ID:", first_sample["label"])

        # Decode the numeric label into its class name.
        label_feature = split_data.features["label"]
        label_name = label_feature.names[first_sample["label"]]
        print("Label name:", label_name)


if __name__ == "__main__":
    main()