from backend.app.services.seed_detector import SEEDDetector


IMAGE_PATH = (
    "data/cache/RealText-V2/train/image/"
    "part010/GenText_Forensic_00015103.jpg"
)


def main():
    detector = SEEDDetector()

    print("Running SEEDDetector...")

    result = detector.predict(IMAGE_PATH)

    print("\nPrediction result:")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.4f}")
    print(f"Real probability: {result['real_probability']:.4f}")
    print(f"Forged probability: {result['forged_probability']:.4f}")

    print("\nLocalization:")
    print(f"Image size: {result['image_width']}x{result['image_height']}")
    print(f"Tampered pixels: {result['tampered_pixels']}")
    print(f"Tamper ratio: {result['tamper_ratio']:.6f}")

    print(
        f"Base64 mask generated: "
        f"{len(result['tamper_mask_base64'])} characters"
    )


if __name__ == "__main__":
    main()