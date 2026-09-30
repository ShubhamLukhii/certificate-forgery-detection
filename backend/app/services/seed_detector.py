from pathlib import Path
from typing import Any
import base64
import io

import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from backend.app.ml.hf_wrapper import EoMTForTamperingDetection




class SEEDDetector:
    """
    Wrapper around the pretrained SEED document forgery detector.

    SEED provides:
    1. Image-level REAL/FORGED classification.
    2. Pixel-level tampering localization.
    """

    MODEL_ID = "Jason37437/SEED"
    IMAGE_SIZE = 512

    def __init__(self) -> None:
        # Use Apple Silicon GPU when available.
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        self.model = None

        # Image preprocessing used before passing the image to SEED.
        self.transform = transforms.Compose(
            [
                transforms.Resize((self.IMAGE_SIZE, self.IMAGE_SIZE)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )
        
    def _mask_to_base64(self, tamper_mask) -> str:
        """Convert a binary tamper mask to a Base64 PNG."""

        mask_image = Image.fromarray(
        (tamper_mask.cpu().numpy().astype("uint8") * 255)
        )
        buffer = io.BytesIO()
        mask_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def load_model(self) -> None:
        """Load the pretrained SEED model."""

        if self.model is not None:
            return

        print(f"Loading SEED model on {self.device}...")

        self.model = EoMTForTamperingDetection.from_pretrained(
            self.MODEL_ID
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        print("SEED model loaded successfully.")

    def predict(self, image_path: str | Path) -> dict[str, Any]:
        """
        Run SEED inference on an image.

        Returns image-level classification and pixel-level
        tampering information.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # Load image.
        image = Image.open(image_path).convert("RGB")

        original_width, original_height = image.size

        # Preprocess image.
        image_tensor = self.transform(image).unsqueeze(0)
        image_tensor = image_tensor.to(self.device)

        # Load model only when inference is actually required.
        self.load_model()

        # Run inference.
        with torch.no_grad():
            outputs = self.model(image_tensor)

        # ---------------------------------------------------------
        # IMAGE-LEVEL CLASSIFICATION
        # ---------------------------------------------------------

        # SEED's fourth output contains image-level logits.
        image_logits = outputs[3]

        probabilities = torch.softmax(image_logits, dim=-1)

        real_probability = probabilities[0, 0].item()
        forged_probability = probabilities[0, 1].item()

        if forged_probability >= real_probability:
            prediction = "FORGED"
            confidence = forged_probability
        else:
            prediction = "REAL"
            confidence = real_probability

        # ---------------------------------------------------------
        # PIXEL-LEVEL TAMpering MASK
        # ---------------------------------------------------------

        # Final mask prediction.
        mask_logits = outputs[0][-1]

        # Convert logits into probabilities.
        mask_probability = torch.sigmoid(mask_logits)

        # Remove batch/query dimensions.
        mask_probability = mask_probability.squeeze(0).squeeze(0)

        # Resize the mask from 128x128 back to original image size.
        mask_probability = F.interpolate(
            mask_probability.unsqueeze(0).unsqueeze(0),
            size=(original_height, original_width),
            mode="bilinear",
            align_corners=False,
        ).squeeze()

        # Binary tampering mask.
        tamper_mask = mask_probability >= 0.5

        # Count tampered pixels.
        tampered_pixels = int(tamper_mask.sum().item())

        total_pixels = original_width * original_height

        tamper_ratio = (
            tampered_pixels / total_pixels
            if total_pixels > 0
            else 0.0
        )

        return {
            "prediction": prediction,
            "confidence": confidence,
            "real_probability": real_probability,
            "forged_probability": forged_probability,
            "image_width": original_width,
            "image_height": original_height,
            "tampered_pixels": tampered_pixels,
            "tamper_ratio": tamper_ratio,
            "mask_width": original_width,
            "mask_height": original_height,
            "tamper_mask_base64": self._mask_to_base64(tamper_mask),
        }