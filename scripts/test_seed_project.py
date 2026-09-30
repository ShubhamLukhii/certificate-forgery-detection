import torch

from backend.app.ml.hf_wrapper import EoMTForTamperingDetection


MODEL_ID = "Jason37437/SEED"


def main():
    # Select Apple Silicon GPU (MPS) if available.
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    print(f"Using device: {device}")
    print("Loading SEED model through project code...")

    model = EoMTForTamperingDetection.from_pretrained(MODEL_ID)

    model = model.to(device)
    model.eval()

    print("SEED model loaded successfully.")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")


if __name__ == "__main__":
    main()