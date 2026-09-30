import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [overlay, setOverlay] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const canvasRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setResult(null);
    setOverlay(null);
    setError("");

    if (!selectedFile) {
      setFile(null);
      setPreview(null);
      return;
    }

    if (!selectedFile.type.startsWith("image/")) {
      setFile(null);
      setPreview(null);
      setError("Please select an image file.");
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const analyzeCertificate = async () => {
    if (!file) {
      setError("Please select a certificate image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setOverlay(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch('/predict', {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
        "Unable to connect to the forgery detection server."
      );
    } finally {
      setLoading(false);
    }
  };

  /*
   * Convert the Base64 mask returned by SEED into a
   * transparent red overlay.
   */
  useEffect(() => {
    if (!result?.tamper_mask_base64 || !preview) {
      return;
    }

    const maskImage = new Image();

    maskImage.onload = () => {
      const canvas = canvasRef.current;

      if (!canvas) {
        return;
      }

      const width = result.image_width;
      const height = result.image_height;

      canvas.width = width;
      canvas.height = height;

      const context = canvas.getContext("2d");

      context.clearRect(0, 0, width, height);

      context.drawImage(
        maskImage,
        0,
        0,
        width,
        height
      );

      const imageData = context.getImageData(
        0,
        0,
        width,
        height
      );

      const pixels = imageData.data;

      /*
       * SEED mask:
       * black  = tampered
       * white  = non-tampered
       *
       * Convert tampered pixels to transparent red.
       */
      for (let i = 0; i < pixels.length; i += 4) {
        const maskValue = pixels[i];

        // White pixels in the SEED mask represent tampered regions.
        if (maskValue > 128) {
          pixels[i] = 255;
          pixels[i + 1] = 60;
          pixels[i + 2] = 60;
          pixels[i + 3] = 120;
        } else {
          // Black pixels are normal/background regions.
          pixels[i + 3] = 0;
        }
      }

      context.putImageData(imageData, 0, 0);

      setOverlay(canvas.toDataURL("image/png"));
    };

    maskImage.src = `data:image/png;base64,${result.tamper_mask_base64}`;
  }, [result, preview]);

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div className="header-content">
          <h1>Certificate Forgery Detector</h1>

          <p>
            AI-powered academic certificate analysis
            using SEED
          </p>
        </div>
      </header>

      <main>

        {/* UPLOAD SECTION */}
        <section className="upload-section">

          <div className="upload-content">

            <div>
              <h2>Analyze a Certificate</h2>

              <p className="section-description">
                Upload a scanned academic certificate to
                detect possible forgery and locate suspicious
                regions.
              </p>
            </div>

            <div className="upload-controls">

              <label className="file-input">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                />

                <span>
                  {file
                    ? file.name
                    : "Choose certificate image"}
                </span>
              </label>

              <button
                className="analyze-button"
                onClick={analyzeCertificate}
                disabled={!file || loading}
              >
                {loading
                  ? "Analyzing Certificate..."
                  : "Analyze Certificate"}
              </button>

            </div>

            {error && (
              <div className="error">
                {error}
              </div>
            )}

          </div>

        </section>


        {/* IMAGE RESULTS */}
        {preview && (
          <section className="visualization-section">

            {/* ORIGINAL */}
            <div className="visual-card">

              <div className="card-header">
                <h2>Original Certificate</h2>
              </div>

              <div className="certificate-view">
                <img
                  src={preview}
                  alt="Uploaded certificate"
                />
              </div>

            </div>


            {/* OVERLAY */}
            <div className="visual-card">

              <div className="card-header">
                <h2>Tamper Localization</h2>

                {result && (
                  <span className="localization-label">
                    Suspicious regions
                  </span>
                )}
              </div>

              <div className="certificate-view">

                {overlay ? (
                  <div className="overlay-wrapper">

                    <img
                      src={preview}
                      alt="Certificate"
                    />

                    <img
                      src={overlay}
                      alt="Transparent tamper localization overlay"
                      className="tamper-overlay"
                    />

                  </div>
                ) : (
                  <div className="empty-result">
                    <span>
                      Run analysis to see suspicious regions
                    </span>
                  </div>
                )}

              </div>

            </div>

          </section>
        )}


        {/* RAW MASK */}
        {result && (
          <section className="mask-section">

            <div className="mask-header">
              <div>
                <h2>SEED Pixel-Level Mask</h2>

                <p>
                  Pixel-level output generated by the
                  pretrained SEED model.
                </p>
              </div>

              <img
                className="raw-mask"
                src={`data:image/png;base64,${result.tamper_mask_base64}`}
                alt="SEED tamper mask"
              />
            </div>

          </section>
        )}


        {/* RESULT */}
        {result && (
          <section className="result-section">

            <div className="result-header">

              <div>
                <span className="result-label">
                  Detection Result
                </span>

                <div
                  className={`prediction ${result.prediction === "FORGED"
                      ? "forged"
                      : "real"
                    }`}
                >
                  {result.prediction}
                </div>
              </div>

              <div className="confidence">
                <span>Confidence</span>

                <strong>
                  {(result.confidence * 100).toFixed(2)}%
                </strong>
              </div>

            </div>


            <div className="metrics">

              <div className="metric">
                <span>Real Probability</span>

                <strong>
                  {(result.real_probability * 100).toFixed(2)}%
                </strong>
              </div>

              <div className="metric">
                <span>Forged Probability</span>

                <strong>
                  {(result.forged_probability * 100).toFixed(2)}%
                </strong>
              </div>

              <div className="metric">
                <span>Tamper Ratio</span>

                <strong>
                  {(result.tamper_ratio * 100).toFixed(4)}%
                </strong>
              </div>

              <div className="metric">
                <span>Tampered Pixels</span>

                <strong>
                  {result.tampered_pixels.toLocaleString()}
                </strong>
              </div>

            </div>

          </section>
        )}

      </main>


      <footer>
        SEED pretrained model
      </footer>

      {/* Hidden canvas used to generate overlay */}
      <canvas
        ref={canvasRef}
        style={{ display: "none" }}
      />

    </div>
  );
}

export default App;