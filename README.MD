# Visual Medical Assistant 🩺

Built by Md Zaheeruddin

A Streamlit web application that leverages Google's Gemini AI (gemini-2.0-flash-exp) to analyze medical images and provide structured insights, recommendations, and treatment suggestions for informational and educational purposes.

---

## Features

- 🖼️ Image Upload: Supports PNG, JPG, and JPEG formats  
- 🤖 AI-Powered Analysis: Uses Google Gemini 2.0 Flash model for medical image interpretation  
- 📊 Structured Output: Provides analysis in four sections:
  - Detailed Analysis
  - Analysis Report
  - Recommendations
  - Treatments
- 🎨 User-Friendly Interface: Clean two-column layout with real-time image preview  
- ⚡ Fast Processing: Loading indicators for better UX

---

## Prerequisites

- Python 3.8 or higher  
- Google API Key for Gemini AI (see Configuration)

---

## Quick Start

Clone the repository (or download the files):

```bash
git clone <https://github.com/Tensor-Titans-Labs/Visual-Medical-Assistant.git>
cd visual-medical-assistant
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

Set up your Google API key (see Configuration), then run:

```bash
streamlit run app.py
```

Open your browser and navigate to: http://localhost:8501

---

## Configuration

This project expects a Google API key for the Gemini model. There are two simple options:

1. File-based (quick, local development)
   - Create a file named `google_api_key.py` in the project root (do NOT commit this file).
   - Add the following content:

```python
# google_api_key.py (example)
google_api_key = "YOUR_API_KEY_HERE"
```

2. Environment variable (recommended for production)
   - Add your API key to an environment variable, e.g.:
     - Linux / macOS:
       ```bash
       export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
       ```
     - Windows (PowerShell):
       ```powershell
       setx GOOGLE_API_KEY "YOUR_API_KEY_HERE"
       ```

Make sure the application reads whichever method you prefer. For local quickstart, `google_api_key.py` is supported by the example app.

Security tip: Add `google_api_key.py` to `.gitignore`.

Example `.gitignore` entry:

```
google_api_key.py
.env
.venv/
```

---

## Gemini Model Configuration

The application uses the following default Gemini settings:

- Model: `gemini-2.0-flash-exp`
- Temperature: `1.0`
- Top P: `0.95`
- Max Output Tokens: `8192`
- Safety Settings: Medium and above blocking for harassment, hate speech, sexually explicit, and dangerous content

Adjust these values in your app configuration if needed.

---

## Usage

1. Start the app: `streamlit run app.py`  
2. Upload an image (PNG, JPG, JPEG) using the "Browse files" button  
3. Click "Generate Analysis" to receive AI-powered insights  
4. Review the four result sections:
   - Detailed Analysis
   - Analysis Report
   - Recommendations
   - Treatments

---

## Project Structure

visual-medical-assistant/
│
├── app.py                  # Main Streamlit application
├── google_api_key.py       # Google API key configuration (not in git)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

(Your repository may contain additional helper modules and assets.)

---

## Troubleshooting

Common issues and fixes:

- API Key Error
  - Ensure your Google API key is valid and configured correctly.
  - If using `google_api_key.py`, confirm it is present and contains the correct variable.
  - If using environment variables, ensure the process running Streamlit can access them.

- Image Upload Fails
  - Verify supported image formats (PNG, JPG, JPEG).
  - Check file size (recommended < 10 MB).
  - Inspect browser console and Streamlit logs for errors.

- No Analysis Generated
  - Verify internet connectivity.
  - Check your Google API quota.
  - Review error messages printed to console and Streamlit logs.

---

## Important Disclaimer

⚠️ Medical Disclaimer: This application is for informational and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making medical decisions.

---

## Security Notes

- Keep your `google_api_key.py` (or any file/secret storing your API key) out of version control.
- Prefer environment variables, secret managers, or vaults in production.
- Rotate API keys regularly and follow principle of least privilege.

---

## Future Enhancements

- Support for multiple image uploads
- Export analysis reports to PDF
- Integration with medical databases
- User authentication and history tracking
- Support for DICOM medical image format
- Multi-language support

---

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue to discuss changes or submit a pull request with detailed description and tests where applicable.

---

## Support

For questions or support, please open an issue in the repository.

---

## License

This project is provided as-is for educational purposes.

---

## Author


Built by Md Zaheeruddin
