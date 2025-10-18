import streamlit as st
from pathlib import Path
import google.generativeai as genai
from google_api_key import google_api_key

# --- Configure Google API ---
genai.configure(api_key=google_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompts = [
    """
    You are a domain expert in medical image analysis. Please provide the final response 
    with these 4 headings: Detailed Analysis, Analysis Report, Recommendations, Treatments.
    """
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# --- Streamlit UI ---
st.set_page_config(
    page_title="Visual Medical Assistant", 
    page_icon="🩺", 
    layout="wide"
)

# Header
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Visual Medical Assistant 🩺</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Analyze medical images and get detailed insights</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-style: italic;'>Built by Md Zaheeruddin</p>", unsafe_allow_html=True)

# --- Two-column layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Upload Your Medical Image")
    file_uploaded = st.file_uploader(
        label="Supported formats: PNG, JPG, JPEG", 
        type=['png','jpg','jpeg'], 
        help="Choose a clear image for accurate analysis"
    )
    
    if file_uploaded:
        st.image(file_uploaded, use_container_width=True, caption='Uploaded Image Preview')
    
    submit = st.button("Generate Analysis", use_container_width=True)

with col2:
    st.subheader("Analysis Output")
    analysis_placeholder = st.empty()

# --- Logic for Analysis ---
if submit:
    if not file_uploaded:
        st.warning("⚠️ Please upload an image first.")
    else:
        with st.spinner("Analyzing image... This may take a few seconds ⏳"):
            try:
                image_data = file_uploaded.getvalue()
                image_parts = [{"mime_type": "image/jpg", "data": image_data}]
                prompt_parts = [image_parts[0], system_prompts[0]]
                
                response = model.generate_content(prompt_parts)
                
                if response:
                    # Structured display
                    analysis_placeholder.markdown("### Detailed Analysis")
                    analysis_placeholder.write(response.text)
                else:
                    analysis_placeholder.error("No response generated. Please try again.")
            
            except Exception as e:
                analysis_placeholder.error(f"Error generating analysis: {e}")

# Footer with disclaimer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Disclaimer: Consult with a Doctor before making any decisions.</p>", unsafe_allow_html=True)
