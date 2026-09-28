from pathlib import Path
from typing import Any

from PIL import Image


class SEEDDetector:
    """
    Wrapper around the pretrained SEED document forgery detector.

    The actual SEED model will be loaded once DINOv3 access
    is available.
    """

    def __init__(self):
        self.model = None
        self.device = None
        self.loaded = False

    def load_model(self) -> None:
        """
        Load the pretrained SEED model.

        This will be implemented after DINOv3 access is available.
        """
        raise NotImplementedError(
            "SEED model loading will be enabled after DINOv3 access "
            "is granted."
        )

    def predict(self, image_path: str | Path) -> dict[str, Any]:
        """
        Run forgery detection on an image.

        Parameters
        ----------
        image_path:
            Path to the certificate image.

        Returns
        -------
        dict
            Prediction results including classification and
            localization information.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # Validate that the uploaded file is actually an image.
        with Image.open(image_path) as image:
            image.verify()

        if not self.loaded:
            raise RuntimeError(
                "SEED model is not currently loaded."
            )

        # Actual SEED inference will be implemented here.
        raise NotImplementedError(
            "SEED inference is not implemented yet."
        )