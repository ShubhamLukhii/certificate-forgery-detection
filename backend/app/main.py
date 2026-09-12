from fastapi import FastAPI

# Create the FastAPI application instance.
app = FastAPI(
    title="Certificate Forgery Detection API",
    description="API for academic certificate forgery detection and tamper localization.",
    version="0.1.0",
)


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