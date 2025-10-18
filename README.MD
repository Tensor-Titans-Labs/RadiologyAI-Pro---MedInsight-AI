# Problem Statement: Visual Medical Assistant

### Context:

In modern healthcare, the demand for quick, accurate, and accessible medical diagnosis is increasing. Medical professionals often face challenges such as time constraints, lack of expertise in analyzing certain medical images, and the need for a second opinion. This project aims to leverage generative AI to provide detailed analysis and recommendations for medical images, assisting healthcare professionals in identifying potential health issues.

### Objective:

To develop a Streamlit-based application, Visual Medical Assistant, that integrates Google's Generative AI capabilities to analyze uploaded medical images and provide a structured report with detailed insights, recommendations, and potential treatments.

### Project Setup

1. Clone the Repository
```bash
git clone <repository-url>
cd smart-ats-resume-analyzer
```

2. Create Virtual Environment
```bash
conda create -p env python=3.10 -y
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Environment Configuration Create a .env file in the root directory:
```bash
GOOGLE_API_KEY =your_api_key_here
```

5. Run the Application
```bash
streamlit run app.py
```