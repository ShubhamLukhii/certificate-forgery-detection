from pathlib import Path
from typing import Any

import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms


class SEEDDetector:
    """
    Wrapper around the pretrained SEED document forgery detector.

    SEED provides:
    - image-level real/forged classification
    - pixel-level tamper localization
    """

    MODEL_ID = "Jason37437/SEED"
    IMAGE_SIZE = 512

    def __init__(self):
        self.model = None
        self.device = (
            torch.device("mps")
            if torch.backends.mps.is_available()
            else torch.device("cpu")
        )

        self.transform = transforms.Compose(
            [
                transforms.Resize(
                    (self.IMAGE_SIZE, self.IMAGE_SIZE)
                ),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

        self.loaded = False

    def load_model(self) -> None:
        """
        Load the pretrained SEED model from Hugging Face.
        """

        from backend.app.ml.hf_wrapper import (
            EoMTForTamperingDetection,
        )

        print(
            f"Loading SEED model on {self.device}..."
        )

        self.model = (
            EoMTForTamperingDetection
            .from_pretrained(self.MODEL_ID)
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        self.loaded = True

        print("SEED model loaded successfully.")

    def predict(
        self,
        image_path: str | Path,
    ) -> dict[str, Any]:
        """
        Run SEED inference on a certificate image.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # Load and validate image.
        image = Image.open(image_path).convert("RGB")

        original_width, original_height = image.size

        # Preprocess.
        image_tensor = self.transform(image)
        image_tensor = image_tensor.unsqueeze(0)
        image_tensor = image_tensor.to(self.device)

        # Load model if necessary.
        if not self.loaded:
            self.load_model()

        # Run inference.
        with torch.no_grad():
            outputs = self.model(image_tensor)

        # ---------------------------------------------
        # Image-level classification
        # ---------------------------------------------

        image_logits = outputs[3]

        image_probabilities = F.softmax(
            image_logits,
            dim=-1,
        )[0]

        # SEED uses two image-level classes:
        # class 0 = real
        # class 1 = forged
        real_probability = float(
            image_probabilities[0].item()
        )

        forged_probability = float(
            image_probabilities[1].item()
        )

        if forged_probability >= real_probability:
            prediction = "forged"
            confidence = forged_probability
        else:
            prediction = "real"
            confidence = real_probability

        # ---------------------------------------------
        # Tamper localization
        # ---------------------------------------------

        mask_logits = outputs[0][-1]

        # Convert logits to probabilities.
        mask_probability = torch.sigmoid(
            mask_logits
        )

        # Remove batch/query dimensions.
        mask_probability = mask_probability[0, 0]

        # Resize mask back to original image size.
        mask_probability = F.interpolate(
            mask_probability.unsqueeze(0).unsqueeze(0),
            size=(original_height, original_width),
            mode="bilinear",
            align_corners=False,
        )[0, 0]

        # Binary tamper mask.
        tamper_mask = (
            mask_probability >= 0.5
        ).cpu()

        tampered_pixels = int(
            tamper_mask.sum().item()
        )

        total_pixels = (
            original_width * original_height
        )

        tamper_ratio = (
            tampered_pixels / total_pixels
            if total_pixels > 0
            else 0.0
        )

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "real_probability": round(
                real_probability,
                4,
            ),
            "forged_probability": round(
                forged_probability,
                4,
            ),
            "image_width": original_width,
            "image_height": original_height,
            "tamper_ratio": round(
                tamper_ratio,
                4,
            ),
            "tampered_pixels": tampered_pixels,
            "mask_width": original_width,
            "mask_height": original_height,
            "tamper_mask": tamper_mask.numpy(),
        }