from pathlib import Path
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.app.services.seed_detector import SEEDDetector


# Create the FastAPI application instance.
app = FastAPI(
    title="Certificate Forgery Detection API",
    description=(
        "API for academic certificate forgery detection "
        "and tamper localization."
    ),
    version="0.1.0",
)


# Create the detector service.
detector = SEEDDetector()


@app.get("/")
def root():
    """
    Basic root endpoint to confirm that the API is running.
    """
    return {
        "message": "Certificate Forgery Detection API is running"
    }


@app.get("/health")
def health_check():
    """
    Health-check endpoint used by tests, deployment systems,
    and monitoring tools.
    """
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict_certificate(
    file: UploadFile = File(...)
):
    """
    Analyze an uploaded certificate image.

    The actual SEED inference will be connected once
    the pretrained model is available.
    """

    # Basic file validation.
    if not file.content_type or not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported.",
        )

    suffix = Path(file.filename or "").suffix

    if not suffix:
        suffix = ".png"

    try:
        # Store the uploaded file temporarily.
        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False,
        ) as temporary_file:

            contents = await file.read()
            temporary_file.write(contents)
            temporary_path = Path(temporary_file.name)

        # Run detector.
        result = detector.predict(temporary_path)

        return result

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    finally:
        # Remove temporary uploaded file.
        if "temporary_path" in locals():
            temporary_path.unlink(
                missing_ok=True
            )