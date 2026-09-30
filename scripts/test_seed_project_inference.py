from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

from backend.app.ml.hf_wrapper import EoMTForTamperingDetection


MODEL_ID = "Jason37437/SEED"

IMAGE_PATH = Path(
    "data/cache/RealText-V2/train/image/part010/GenText_Forensic_00015103.jpg"
)

IMAGE_SIZE = 512


def main():
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    device = torch.device(
        "mps" if torch.backends.mps.is_available() else "cpu"
    )

    print(f"Using device: {device}")
    print(f"Loading image: {IMAGE_PATH}")

    image = Image.open(IMAGE_PATH).convert("RGB")

    print(f"Original image size: {image.size}")

    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    image_tensor = transform(image).unsqueeze(0).to(device)

    print(f"Input tensor shape: {image_tensor.shape}")

    print("Loading SEED model...")

    model = EoMTForTamperingDetection.from_pretrained(MODEL_ID)
    model = model.to(device)
    model.eval()

    print("Running inference...")

    with torch.no_grad():
        outputs = model(image_tensor)

    print("Inference completed successfully.")
    print(f"Number of output groups: {len(outputs)}")

    # Image-level logits
    image_logits = outputs[3]

    probabilities = torch.softmax(image_logits, dim=-1)

    real_probability = probabilities[0, 0].item()
    forged_probability = probabilities[0, 1].item()

    print("\nImage-level prediction:")
    print(f"Real probability:   {real_probability:.4f}")
    print(f"Forged probability: {forged_probability:.4f}")

    if forged_probability >= real_probability:
        prediction = "FORGED"
    else:
        prediction = "REAL"

    print(f"Prediction: {prediction}")

    # Final pixel-level mask
    mask_logits = outputs[0][-1]

    print("\nFinal mask:")
    print(f"Mask logits shape: {mask_logits.shape}")

    mask_probability = torch.sigmoid(mask_logits)

    print(
        f"Mask probability range: "
        f"{mask_probability.min().item():.4f} - "
        f"{mask_probability.max().item():.4f}"
    )


if __name__ == "__main__":
    main()