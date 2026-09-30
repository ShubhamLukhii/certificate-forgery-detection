# CNN-Based Academic Certificate Forgery Detection Using Residual Learning and Pixel-Level Tamper Localization

An AI-based system for detecting potential forgery in scanned academic certificates and identifying potentially tampered regions at pixel level.

> **Current MVP:** The publicly deployed temporary MVP uses the pretrained **SEED** tampering detector. The long-term project roadmap remains focused on developing and evaluating a custom Residual CNN-based certificate forgery detection system.

---

## Live Demo

**Live application:**  
http://13.206.240.176:8001

The current MVP is deployed on **AWS EC2** and provides certificate upload, forgery classification, confidence/probability information, and pixel-level tamper localization.

---

## Project Overview

Academic certificates are increasingly exchanged in digital form, making image/document manipulation a practical concern. This project aims to develop a deep-learning-based system that can:

1. Analyze scanned academic certificates.
2. Determine whether a certificate is likely to be pristine or forged.
3. Estimate the confidence of the classification.
4. Identify potentially tampered regions at pixel level.
5. Present the result through a web-based interface.
6. Provide a deployable inference pipeline that can later be replaced or extended with models trained specifically for this project.

The project is being developed as a research-oriented system with separate stages for dataset preparation, model development, localization, API integration, frontend development, testing, security/privacy considerations, and deployment.

---

## Current Objectives

### Completed / Implemented

- Dataset acquisition and validation
- Original dataset metadata inspection
- Training metadata preparation
- Pretrained SEED model integration
- CPU/GPU/MPS-aware model device selection
- Certificate image preprocessing
- Image-level forgery classification
- Pixel-level tamper mask generation
- Tamper mask resizing to original image dimensions
- Tampered-pixel counting
- Tamper-ratio calculation
- Base64 mask transfer through the API
- FastAPI inference API
- React + Vite frontend
- Certificate upload and preview
- Prediction result display
- Tamper localization visualization
- Production React build
- FastAPI-served React frontend
- AWS EC2 deployment
- ARM64 CPU deployment
- Hugging Face authentication for gated DINOv3 access
- Persistent deployment using systemd
- Public MVP availability

### Planned Long-Term Work

- Dataset analysis and deeper distribution studies
- Preprocessing and augmentation experiments
- Train/validation/test split strategy
- Baseline CNN
- Custom Residual CNN architecture
- Model training and evaluation
- Pixel-level localization experiments
- Model comparison and ensemble approaches
- Combined custom-model inference
- Comprehensive evaluation/error analysis
- Security and privacy implementation
- Extended testing
- CI/CD improvements
- Final deployment architecture
- Final validation and documentation

---

#  Dataset

## RealText-V2

The project currently uses **RealText-V2** from Hugging Face:

`vankey/RealText-V2`

The dataset is designed for multilingual text/document forgery analysis and contains:

- 20K+ images
- 6 languages
- 6 domains
- Multiple forgery types
- Multi-source samples
- Pixel-level localization masks

The dataset includes both pristine and forged samples and provides masks for samples where localization information is available.

### Dataset Metadata

The project inspected the original metadata rather than relying on automatically generated dataset labels.

The inspected metadata contains:

```text
sample_id
language
language_code
type
image_file
mask_file
has_mask
report_file
report_text
```

The prepared training metadata currently contains:

- **13,500 training records**
- **7,500 forged samples**
- **6,000 pristine samples**
- **7,500 samples with masks**

Image and mask paths were validated during metadata preparation.

---

#  Dataset Preparation

The dataset is cached locally rather than committed to GitHub.

Dataset-related files are intentionally excluded from Git because of their size.

### Dataset cache

```text
data/cache/RealText-V2/
```

### Generated training metadata

```text
data/processed/training_metadata.csv
```

The generated metadata file is also excluded from Git.

### Metadata inspection

```text
scripts/inspect_metadata.py
```

This script was used to inspect:

- Metadata shape
- Metadata columns
- Data types
- Authenticity distribution
- Mask availability
- Language distribution
- Example image paths
- Example mask paths

### Training metadata preparation

```text
scripts/prepare_training_metadata.py
```

This script creates the validated training metadata used as the basis for future model training.

---

#  Current MVP Model — SEED

The temporary MVP uses the pretrained:

**Jason37437/SEED**

SEED provides:

- Image-level tampering classification
- Pixel-level tamper localization

### SEED architecture used by the MVP

- DINOv3 ViT-L/16 backbone
- LoRA rank 1
- One mask query
- Four decoder blocks
- 512 × 512 model input
- Approximately 304M parameters

The SEED checkpoint is approximately 1.2 GB.

### Model source

Hugging Face:  
https://huggingface.co/Jason37437/SEED

Official repository:  
https://github.com/KahimWong/SEED

---

#  Hugging Face / DINOv3 Access

SEED uses the gated DINOv3 backbone:

```text
facebook/dinov3-vitl16-pretrain-lvd1689m
```

The EC2 deployment therefore requires an authenticated Hugging Face account with access to the gated DINOv3 model.

The model is downloaded and cached on the deployment server after authentication.

**Hugging Face tokens must never be committed to the repository.**

---

#  SEED Integration

The integrated SEED implementation is located under:

```text
backend/app/ml/
```

Current files include:

```text
__init__.py
cfg.py
eomt_sep_query.py
hf_wrapper.py
lora.py
mask_classification_loss.py
scale_block.py
```

The project uses its own package imports so that the SEED implementation can be loaded from the FastAPI application.

---

#  Inference Pipeline

```text
Certificate Image
       │
       ▼
FastAPI Upload
       │
       ▼
Temporary Image File
       │
       ▼
SEED Detector
       │
       ├───────────────┐
       ▼               ▼
Classification      Mask Prediction
       │               │
       ▼               ▼
REAL / FORGED     Pixel-level Mask
       │               │
       └───────┬───────┘
               ▼
        Result Processing
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
 Confidence  Tamper   Localization
             Ratio       Mask
               │
               ▼
          JSON Response
               │
               ▼
          React Frontend
```

### API output

The API currently returns information including:

```text
prediction
confidence
real_probability
forged_probability
image_width
image_height
tampered_pixels
tamper_ratio
mask_width
mask_height
tamper_mask_base64
```

The binary mask is encoded as Base64 for API transfer and frontend rendering.

---

#  Example Inference

A locally tested RealText-V2 sample produced:

```text
Prediction: REAL
Confidence: 0.5862
Real probability: 0.5862
Forged probability: 0.4138
Image size: 1191 × 1684
Tampered pixels: 28439
Tamper ratio: 0.014179
```

Another tested sample produced approximately:

```text
Forged probability: 0.961267
Real probability: 0.038733
Tamper ratio: 0.0017265
```

These are individual inference examples and should not be interpreted as overall model accuracy.

---

#  Backend

The backend uses **FastAPI**.

Main application:

```text
backend/app/main.py
```

Detector:

```text
backend/app/services/seed_detector.py
```

The detector supports:

- Lazy model loading
- CPU inference
- CUDA detection
- Apple Silicon MPS detection
- Image preprocessing
- Classification
- Localization
- Mask resizing
- Base64 mask encoding

### API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serves the React production frontend |
| `/health` | GET | Backend health check |
| `/predict` | POST | Certificate forgery prediction and tamper localization |

### Health response

```json
{
  "status": "healthy"
}
```

---

#  Frontend

The frontend uses:

- React
- Vite
- JavaScript
- CSS

Location:

```text
frontend/
```

Current features:

- Certificate upload
- Image preview
- Analyze button
- Prediction result
- Confidence
- Real probability
- Forged probability
- Tampered-pixel count
- Tamper ratio
- Potentially tampered-region visualization
- Raw binary mask visualization

The frontend uses the relative API path:

```javascript
fetch("/predict", ...)
```

This allows the production build to work with FastAPI without hard-coding the backend host.

---

#  Tamper Localization

The UI presents localized areas as:

**Potentially Tampered Regions**

rather than treating the mask as definitive proof of forgery.

Current mask interpretation:

```text
255 / white → potentially tampered
0 / black   → not highlighted
```

A transparent overlay is generated over the original certificate.

---

#  Production Architecture

```text
                    Internet
                       │
                       ▼
             AWS EC2 Public IP
                       │
                       ▼
                 FastAPI :8001
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
     React Frontend              API
                                    │
                                 /predict
                                    │
                                    ▼
                              SEED Detector
                                    │
                              DINOv3 Backbone
                                    │
                                    ▼
                              JSON + Mask
```

The production React build is copied into:

```text
backend/app/static/
```

and served directly by FastAPI.

The generated static directory is intentionally ignored by Git and recreated during deployment.

---

#  AWS Deployment

The temporary MVP is deployed on **AWS EC2**.

| Component | Configuration |
|---|---|
| Region | Mumbai (`ap-south-1`) |
| Instance | `t4g.small` |
| Architecture | ARM64 / `aarch64` |
| RAM | ~1.8 GiB |
| Swap | 4 GiB |
| Storage | 30 GiB gp3 |
| Inference | CPU |
| Backend | FastAPI |
| Frontend | React/Vite production build |
| Process manager | systemd |
| Public port | 8001 |

### CPU-only PyTorch

The EC2 instance uses CPU-only PyTorch. This avoids the large CUDA dependencies that a normal Linux ARM64 PyTorch installation attempted to download.

---

#  Persistent Deployment

FastAPI is managed with:

```text
/etc/systemd/system/certificate-forgery.service
```

The service runs the project's virtual-environment Uvicorn process with:

```text
backend.app.main:app
--host 0.0.0.0
--port 8001
```

It is configured to restart automatically and start after system boot.

The application therefore remains available after the SSH session is closed.

---

#  Security and Deployment Notes

The current deployment is an MVP rather than the final production security architecture.

Current considerations:

- Hugging Face credentials are stored on the deployment server and are not committed to Git.
- Dataset files are excluded from Git.
- Model checkpoints are excluded from Git.
- Python virtual environments are excluded from Git.
- Uploaded files are temporarily stored during inference and removed afterward.
- The API validates that uploaded content is an image.
- CORS was configured for local development/preview environments.
- EC2 currently exposes port `8001`.

### Future security improvements

- HTTPS
- Reverse proxy such as Nginx
- Domain name
- TLS certificate
- Restrictive security-group rules
- Rate limiting
- Stronger file-type and upload-size validation
- Production secret management
- Structured logging
- Monitoring and alerting

---

#  Testing and CI/CD

The project has backend tests under:

```text
backend/tests/
```

The existing test suite has successfully run with:

```text
2 passed
```

GitHub Actions is used for continuous testing and backend validation.

The CI configuration also accounts for GitHub Actions runtime changes, including the Node.js 20 deprecation affecting older actions.

---

#  Git Workflow

Development follows an issue → branch → PR workflow.

The temporary deployment was implemented on:

```text
feature/temporary-mvp-deployment
```

The branch was pushed to GitHub and deployed to EC2.

Generated files such as:

```text
backend/app/static/
```

are excluded from Git because they are deployment artifacts generated from the React build.

---

#  Project Structure

```text
certificate-forgery-detection/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── services/
│   │   │   └── seed_detector.py
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── cfg.py
│   │   │   ├── eomt_sep_query.py
│   │   │   ├── hf_wrapper.py
│   │   │   ├── lora.py
│   │   │   ├── mask_classification_loss.py
│   │   │   └── scale_block.py
│   │   └── static/
│   │       └── ... generated React production build ...
│   │
│   └── tests/
│       └── test_main.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── ...
│
├── scripts/
│   ├── inspect_metadata.py
│   └── prepare_training_metadata.py
│
├── data/
│   ├── cache/
│   │   └── RealText-V2/
│   └── processed/
│       └── training_metadata.csv
│
├── .gitignore
├── README.md
└── ...
```

---

#  Local Development

## Backend

Create/activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Run FastAPI:

```bash
PYTHONPATH=. uvicorn backend.app.main:app --port 8001
```

For the single-server production-style setup, the React production build can be copied into:

```text
backend/app/static/
```

and the application can then be accessed through:

```text
http://127.0.0.1:8001
```

## Frontend

From:

```text
frontend/
```

install dependencies:

```bash
npm install
```

Start development mode:

```bash
npm run dev
```

Build production files:

```bash
npm run build
```

Then copy the resulting `frontend/dist/` contents to:

```text
backend/app/static/
```

for the FastAPI-served deployment architecture.

---

#  Long-Term Roadmap

## Phase 1 — Dataset

- [x] Acquire RealText-V2
- [x] Cache dataset locally
- [x] Inspect original metadata
- [x] Validate image/mask paths
- [x] Generate training metadata
- [ ] Perform deeper dataset analysis
- [ ] Define preprocessing strategy
- [ ] Define train/validation/test split
- [ ] Define augmentation pipeline

## Phase 2 — Baseline Models

- [ ] Establish baseline CNN
- [ ] Train baseline model
- [ ] Evaluate classification performance
- [ ] Analyze errors

## Phase 3 — Residual CNN

- [ ] Design residual architecture
- [ ] Implement residual blocks
- [ ] Train custom model
- [ ] Tune hyperparameters
- [ ] Evaluate performance
- [ ] Compare against baseline

## Phase 4 — Pixel-Level Localization

- [ ] Implement localization architecture
- [ ] Train using available masks
- [ ] Evaluate localization quality
- [ ] Analyze false-positive and false-negative regions

## Phase 5 — Model Integration

- [x] Temporary SEED inference integration
- [x] FastAPI inference endpoint
- [x] React integration
- [ ] Integrate custom Residual CNN
- [ ] Compare multiple models
- [ ] Investigate ensemble approaches
- [ ] Build combined inference pipeline

## Phase 6 — Evaluation

Future evaluation should include:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC where appropriate
- Confusion matrix
- Pixel-level localization metrics
- Error analysis

## Phase 7 — Security and Privacy

- [ ] Secure upload pipeline
- [ ] Input validation improvements
- [ ] Rate limiting
- [ ] Secure secret management
- [ ] HTTPS
- [ ] Privacy-aware image handling
- [ ] Logging and monitoring
- [ ] Production security review

## Phase 8 — Final Deployment

- [x] Temporary EC2 MVP
- [ ] Production reverse proxy
- [ ] HTTPS/domain
- [ ] Improved resource management
- [ ] Production monitoring
- [ ] Final trained model deployment
- [ ] Final end-to-end validation

---

# Current Limitations

The current public deployment should be considered a **temporary MVP**.

1. The deployed detector is pretrained SEED rather than the final custom Residual CNN.
2. The EC2 instance performs inference on CPU.
3. The deployment currently uses a public IP and port `8001`.
4. HTTPS/domain configuration has not yet been added.
5. The final custom model has not yet been trained.
6. Comprehensive model evaluation remains part of the research work.
7. Localization identifies potentially tampered regions and should not be treated as definitive proof of fraud.
8. Production-grade security hardening remains to be completed.

---

#  Current Status

**Temporary MVP: DEPLOYED AND WORKING**

Live application:

http://13.206.240.176:8001

The next major milestone is implementation, training, evaluation, and integration of the project's custom Residual CNN-based forgery detection pipeline.
