# CNN-Based Academic Certificate Forgery Detection

A deep learning-based system for detecting forged academic certificates and identifying potentially tampered regions using convolutional neural networks, residual learning, and pixel-level tamper localization.

---

## Project Overview

Academic certificate forgery is a significant concern for educational institutions, employers, and verification authorities. Manually verifying certificates can be time-consuming and may not reliably detect sophisticated image-level alterations.

This project aims to develop an intelligent certificate analysis system that can:

- Classify an uploaded academic certificate as genuine or forged.
- Identify regions that may contain tampering.
- Produce a pixel-level tampering mask.
- Provide prediction results through an API.
- Offer a web-based interface for certificate analysis.
- Apply automated testing to backend, frontend, data-processing, and machine-learning components.
- Follow software engineering practices such as version control, continuous integration, and reproducible experimentation.

The project combines deep learning and cybersecurity concepts to support the analysis and verification of digital certificate images.

> **Note:** This system is intended as an assistive analysis tool and should not replace official certificate verification procedures or expert review.

---

## Objectives

The primary objectives of this project are:

1. Develop a CNN-based certificate forgery classification model.
2. Incorporate residual learning to improve feature extraction and training stability.
3. Detect potentially manipulated or forged certificate images.
4. Localize suspicious regions using pixel-level tampering masks.
5. Evaluate the model using suitable classification and localization metrics.
6. Investigate multiple-model or ensemble-learning approaches to reduce dependence on a single model.
7. Expose the trained model through a FastAPI backend.
8. Develop a frontend interface for uploading certificates and viewing prediction results.
9. Implement automated unit, integration, and end-to-end testing for backend and frontend components.
10. Implement continuous integration using GitHub Actions.
11. Maintain a reproducible dataset preparation, training, and evaluation pipeline.
12. Document the system's performance, limitations, security considerations, and future improvements.

---

## Proposed System Architecture

The planned system will contain the following components:

```text
                    Certificate Image
                           |
                           v
                  Frontend Upload Interface
                           |
                           v
                    FastAPI Backend
                           |
                           v
                   Input Validation
                           |
                           v
                  Image Preprocessing
                           |
                           v
                  Deep Learning Models
                    /             \
                   /               \
                  v                 v
       Forgery Classification   Tamper Localization
                  |                 |
                  v                 v
          Genuine / Forged     Predicted Mask
                  \                 /
                   \               /
                    v             v
                  Result Processing
                           |
                           v
                  Frontend Results View
```

The final system may use multiple models or an ensemble strategy to reduce dependence on a single model and improve reliability.

---

## Dataset

This project uses the **RealText-V2** dataset available through Hugging Face.

### Dataset Information

- **Dataset:** `vankey/RealText-V2`
- **Platform:** Hugging Face
- **Dataset Type:** Multilingual document forgery analysis
- **License:** CC-BY-NC-4.0

The dataset license and usage restrictions should be reviewed before any public or commercial deployment.

### Dataset Characteristics

The dataset provides:

- Document images.
- Authenticity labels.
- Language information.
- Mask filenames.
- Mask availability information.
- Forgery-related reports.
- Pixel-level masks for forged samples.

The dataset contains multiple languages and document domains, including education-related samples.

### Dataset Labels

The metadata uses the following authenticity labels:

| Original Label | Meaning | Numerical Label |
| `white` | Genuine or pristine sample | `0` |
| `black` | Forged or manipulated sample | `1` |

### Dataset Distribution

The inspected metadata contains:

| Total records | 13,500 |
| Genuine samples | 6,000 |
| Forged samples | 7,500 |
| Samples with masks | 7,500 |
| Samples without masks | 6,000 |

### Language Distribution


| English | 3,000 |
| Chinese | 3,000 |
| Thai | 2,000 |
| Malay | 2,000 |
| Indonesian | 2,000 |
| Arabic | 1,500 |

### Dataset Storage

The dataset is downloaded and cached locally. Raw dataset files are not committed to GitHub because of their size and licensing considerations.

Expected local dataset location:

```text
data/cache/RealText-V2/
```

The project will use scripts to allow other users to download or prepare the dataset locally.

---

## Current Project Status

- [x] Created the GitHub repository.
- [x] Configured the initial project structure.
- [x] Created a Python virtual environment.
- [x] Configured the project `.gitignore`.
- [x] Set up Git and GitHub repository integration.
- [x] Created the FastAPI backend.
- [x] Added the root API endpoint.
- [x] Added the health-check endpoint.
- [x] Added backend tests using pytest.
- [x] Verified that the backend tests pass locally.
- [x] Created a GitHub Actions continuous integration workflow.
- [x] Configured CI to install dependencies and run tests.
- [x] Updated GitHub Actions versions to avoid the Node.js 20 deprecation warning.
- [x] Created the `feature/dataset-preparation` development branch.
- [x] Selected the RealText-V2 dataset.
- [x] Downloaded and cached the dataset locally.
- [x] Inspected the dataset metadata.
- [x] Verified metadata shape, columns, labels, mask availability, and language distribution.
- [ ] Create the training metadata preparation script.
- [ ] Map metadata filenames to actual local image and mask paths.
- [ ] Validate image and mask availability.
- [ ] Create stratified training, validation, and testing splits.
- [ ] Build the image loading and preprocessing pipeline.
- [ ] Establish unit tests for dataset preparation and preprocessing components.
- [ ] Expand the testing strategy to cover all future Python components.
- [ ] Visualize genuine images, forged images, and tampering masks.
- [ ] Build a baseline CNN classifier.
- [ ] Train and evaluate the baseline model.
- [ ] Implement a residual CNN architecture.
- [ ] Implement pixel-level tamper localization.
- [ ] Evaluate classification and localization performance.
- [ ] Investigate ensemble or multi-model strategies.
- [ ] Implement model inference utilities.
- [ ] Integrate the trained model with FastAPI.
- [ ] Develop the frontend interface.
- [ ] Add frontend unit testing.
- [ ] Add frontend component and integration testing.
- [ ] Add backend integration and end-to-end testing.
- [ ] Expand GitHub Actions CI workflows.
- [ ] Document experimental results and limitations.
- [ ] Prepare the final demonstration and research documentation.

---

## Planned Project Structure

The project structure will evolve as additional components are implemented.

```text
certificate-forgery-detection/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   └── tests/
│       └── test_main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   │
│   └── tests/
│       └── ...
│
├── data/
│   ├── cache/
│   │   └── RealText-V2/
│   │
│   └── metadata/
│
├── scripts/
│   ├── inspect_dataset.py
│   └── prepare_training_metadata.py
│
├── models/
│   └── ...
│
├── tests/
│   ├── test_metadata.py
│   ├── test_preprocessing.py
│   ├── test_dataset.py
│   ├── test_models.py
│   └── test_inference.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── ...
```

The `frontend`, `models`, and additional testing files will be added when their respective development stages begin.

---

## Backend API

The project currently includes a FastAPI backend.

### Run the Backend

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the development server:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

### Current Endpoints

#### Root Endpoint

```http
GET /
```

Example response:

```json
{
  "message": "Certificate Forgery Detection API is running"
}
```

#### Health Endpoint

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Planned Prediction Endpoint

A prediction endpoint will be added after the model inference pipeline is implemented.

Planned endpoint:

```http
POST /predict
```

The endpoint is expected to accept a certificate image and return:

- Predicted class.
- Confidence score.
- Tampering detection result.
- Predicted tampering mask or a reference to the generated mask.

The final response structure will be documented after implementation.

---

## Testing Strategy

Automated testing is a core part of this project. Tests will be developed alongside each component rather than being added only after the complete system is built.

The testing strategy will cover backend functionality, frontend behavior, data-processing utilities, machine-learning components, inference, and the complete application workflow.

### Testing Levels

```text
Unit Tests
    |
    v
Component Tests
    |
    v
Integration Tests
    |
    v
End-to-End Tests
    |
    v
Continuous Integration
```

### Backend and Python Testing

Python components will be tested using:

- `pytest`
- `pytest-cov`
- `HTTPX`
- `unittest.mock`
- PyTorch testing utilities

Planned Python test coverage includes:

- Metadata preparation.
- File-path resolution.
- Metadata validation.
- Image preprocessing.
- Mask preprocessing.
- Dataset loading.
- DataLoader behavior.
- CNN model forward passes.
- Residual block behavior.
- Model input and output shapes.
- Training utilities.
- Loss calculations.
- Metric calculations.
- Checkpoint saving and loading.
- Inference functions.
- Prediction response formatting.
- FastAPI endpoints.
- Invalid input and error handling.

### Frontend Testing

The frontend will also include automated testing.

Depending on the final frontend stack, the planned testing tools may include:

- Vitest or Jest for JavaScript/TypeScript unit testing.
- React Testing Library for testing React components and user interactions.
- A suitable browser-testing tool, such as Playwright, for end-to-end testing.

Frontend tests will cover:

- Component rendering.
- File-upload behavior.
- File-type and file-size validation.
- Loading states.
- Error messages.
- API request handling.
- Prediction result rendering.
- Confidence display.
- Tampering-mask display.
- Navigation and page behavior.
- Accessibility-related behavior where practical.

Frontend tests should focus on user-visible behavior rather than testing implementation details unnecessarily.

### Integration Testing

Integration tests will verify that multiple components work together correctly.

Examples include:

- Metadata preparation and dataset loading.
- Dataset loading and preprocessing.
- Preprocessing and model inference.
- Inference and FastAPI response generation.
- Frontend API service and backend endpoint.
- Frontend upload component and prediction-result component.

### End-to-End Testing

End-to-end testing will verify the complete user workflow:

```text
Open Web Application
        |
        v
Upload Certificate
        |
        v
Validate File
        |
        v
Send Image to API
        |
        v
Run Model Inference
        |
        v
Receive Prediction
        |
        v
Display Classification and Tampering Regions
```

The end-to-end tests will use controlled test inputs and mocked or lightweight model responses when appropriate.

### Testing Without the Full Dataset

Tests should not depend on the complete downloaded dataset or a fully trained model.

Instead, the project will use:

- Small synthetic images.
- Temporary directories.
- Mock metadata.
- Test fixtures.
- Mock model outputs.
- Lightweight test models.

This ensures that tests remain fast, reproducible, and suitable for GitHub Actions.


## Continuous Integration and CI/CD

GitHub Actions is used to run automated checks whenever changes are pushed or pull requests are created.

### Current CI Pipeline

The current workflow:

1. Checks out the repository.
2. Sets up Python.
3. Upgrades pip.
4. Installs dependencies.
5. Runs pytest.

Workflow file:

```text
.github/workflows/ci.yml
```

### Planned CI Improvements

The CI pipeline will gradually be expanded to include:

- Python unit tests.
- Python code coverage.
- Dataset utility tests.
- Model architecture tests.
- Backend integration tests.
- Frontend dependency installation.
- Frontend unit tests.
- Frontend build verification.
- Frontend linting.
- Frontend coverage reporting.
- API integration tests.
- End-to-end tests where appropriate.

The full dataset and trained model files will not be downloaded during every CI run. CI will use small fixtures and mocked components wherever possible.

---

## Machine Learning Pipeline

The planned machine-learning pipeline is:

```text
Dataset Download
       |
       v
Metadata Preparation
       |
       v
Train/Validation/Test Split
       |
       v
Image and Mask Preprocessing
       |
       v
Dataset Loader
       |
       v
Baseline CNN
       |
       v
Residual CNN
       |
       v
Tamper Localization Model
       |
       v
Model Evaluation
       |
       v
Inference Pipeline
       |
       v
FastAPI Integration
```

---

## Classification Model

The classification model will determine whether a certificate image is genuine or forged.

The initial baseline may follow a structure similar to:

```text
Input Image
    ↓
Convolution
    ↓
Activation Function
    ↓
Pooling
    ↓
Convolution
    ↓
Activation Function
    ↓
Pooling
    ↓
Fully Connected Layer
    ↓
Genuine / Forged
```

After establishing a baseline, residual learning will be introduced.

### Residual Learning

A residual block learns a transformation and adds the original input through a shortcut connection:

\[
y = F(x) + x
\]

where:

- \(x\) is the input.
- \(F(x)\) is the transformation learned by the convolutional layers.
- \(y\) is the output of the residual block.

Residual connections may help improve gradient flow and training stability in deeper networks.

---

## Pixel-Level Tamper Localization

Classification determines whether an image is likely forged, while localization attempts to identify the regions containing possible manipulation.

The planned localization architecture may use an encoder-decoder or U-Net-inspired design with residual components.

```text
Input Certificate
       |
       v
Feature Extraction
       |
       v
Encoder
       |
       v
Bottleneck
       |
       v
Decoder
       |
       v
Predicted Tampering Mask
```

The predicted mask is expected to represent:

```text
0 = Non-tampered region
1 = Potentially tampered region
```

The exact mask representation will depend on the final model implementation.

---

## Model Evaluation

### Classification Metrics

The classification model will be evaluated using:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- ROC-AUC, where applicable.

Special attention will be given to recall for forged certificates because incorrectly classifying a forged certificate as genuine is an important failure case.

### Localization Metrics

The tamper localization component may be evaluated using:

- Pixel accuracy.
- Pixel-level precision.
- Pixel-level recall.
- Intersection over Union, or IoU.
- Dice coefficient.

Visual comparisons will also be performed between:

1. Original certificate image.
2. Ground-truth tampering mask.
3. Predicted tampering mask.
4. Overlay of predicted suspicious regions on the original image.

---

## Technologies

### Programming Language

- Python

### Backend

- FastAPI
- Uvicorn

### Data Processing

- pandas
- NumPy
- Pillow
- PyArrow

### Deep Learning

- PyTorch
- Torchvision

### Machine Learning Utilities

- scikit-learn

### Backend Testing

- pytest
- pytest-cov
- HTTPX
- unittest.mock

### Frontend

- React
- JavaScript or TypeScript

### Frontend Testing

- Vitest or Jest
- React Testing Library
- Playwright or another suitable browser-testing framework

### DevOps and Version Control

- Git
- GitHub
- GitHub Actions

---

## Security and Privacy Considerations

Since certificate images may contain personally identifiable information, the project will consider the following security concerns:

- Secure handling of uploaded files.
- File-type and file-size validation.
- Protection against malicious file uploads.
- Avoiding unnecessary storage of uploaded certificates.
- Controlled access to prediction results.
- Secure API communication.
- Protection of environment variables and secrets.
- Avoiding sensitive information in application logs.
- Appropriate retention and deletion policies.
- Access control for stored files and results.

The system should not expose uploaded certificate images or prediction data unnecessarily.

---

## Reproducibility

The dataset and trained model files are not stored directly in the GitHub repository.

The project will provide scripts and instructions for:

1. Installing dependencies.
2. Downloading or accessing the dataset.
3. Preparing metadata.
4. Creating dataset splits.
5. Training the models.
6. Evaluating the models.
7. Running the prediction API.
8. Running the frontend.
9. Running automated tests.

This approach keeps the repository lightweight and avoids committing large data or model files.

---

## Limitations

Potential limitations include:

- Dataset distribution may not fully represent real-world academic certificates.
- Model predictions may be affected by image quality, compression, scanning artifacts, or unseen forgery techniques.
- A high classification score does not guarantee reliable real-world certificate verification.
- Localization predictions may not perfectly identify every tampered pixel.
- Ensemble models may increase computational requirements and inference time.
- False positives may cause genuine certificates to be flagged for additional review.
- The system should be used as an assistive tool alongside official verification procedures.

---

## Future Scope

Potential future improvements include:

- Ensemble learning using multiple CNN or transformer-based models.
- Confidence calibration and uncertainty estimation.
- Improved pixel-level localization.
- Detection of new and unseen forgery techniques.
- Support for more document formats.
- Integration with institutional certificate verification systems.
- Explainable AI methods for highlighting important evidence.
- Privacy-preserving or secure document processing.
- Secure storage and controlled access to uploaded certificates.
- Audit logging for verification activities.
- Integration with external identity or credential verification APIs, where legally and technically appropriate.
- Human-in-the-loop review for uncertain predictions.
- Personalized verification workflows based on institutional requirements.
- Model monitoring and periodic retraining.
- Deployment optimization for CPU, GPU, or Apple Silicon environments.

---

## Disclaimer

This project is developed for academic and research purposes. Predictions generated by the system should not be treated as definitive proof of fraud. Official verification, institutional records, and expert review remain necessary for high-stakes decisions.