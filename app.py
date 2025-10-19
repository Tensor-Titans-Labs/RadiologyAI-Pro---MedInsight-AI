import streamlit as st
from pathlib import Path
import google.generativeai as genai
from google_api_key import google_api_key
from datetime import datetime
import io

# --- Streamlit UI Configuration (MUST BE FIRST) ---
st.set_page_config(
    page_title="Visual Medical Assistant", 
    page_icon="🩺", 
    layout="centered"
)

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

# --- Custom CSS for better UI ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .upload-section {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .analysis-section {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        min-height: 400px;
    }
    .element-container {
        margin-bottom: 0 !important;
    }
    div[data-testid="column"]:nth-of-type(2) .element-container:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    .sidebar-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .instruction-item {
        display: flex;
        align-items: start;
        margin-bottom: 15px;
        padding: 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    .instruction-number {
        background: white;
        color: #667eea;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
        flex-shrink: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #667eea; font-size: 3em; margin-bottom: 10px;'>🩺 Visual Medical Assistant</h1>
        <p style='color: #666; font-size: 1.2em; margin-bottom: 5px;'>AI-Powered Medical Image Analysis</p>
        <p style='color: #999; font-size: 0.9em; font-style: italic;'>Built with ❤️ by Md Zaheeruddin (Zaheer JK)</p>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar with Instructions ---
with st.sidebar:
    st.markdown("""
        <div class='sidebar-section'>
            <h2 style='margin-top: 0; color: white;'>📋 How to Use</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='instruction-item'>
            <div class='instruction-number'>1</div>
            <div><strong>Upload Image:</strong><br/>Select a clear medical image (X-ray, MRI, CT scan, prescription, etc.)</div>
        </div>
        <div class='instruction-item'>
            <div class='instruction-number'>2</div>
            <div><strong>Generate Analysis:</strong><br/>Click the button to process your image with AI</div>
        </div>
        <div class='instruction-item'>
            <div class='instruction-number'>3</div>
            <div><strong>Review Results:</strong><br/>Read the detailed analysis, report, and recommendations</div>
        </div>
        <div class='instruction-item'>
            <div class='instruction-number'>4</div>
            <div><strong>Download Report:</strong><br/>Save the complete report as a text file for your records</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        ### 💡 Best Practices
        
        ✅ Use high-resolution images  
        ✅ Ensure good lighting  
        ✅ Avoid blurry or unclear photos  
        ✅ Include the entire relevant area  
        
        ### ⚠️ Important Notes
        
        🔒 Your images are processed securely  
        🔍 AI analysis is not a substitute for professional medical advice  
        👨‍⚕️ Always consult with a healthcare provider  
        """)
    
    st.markdown("---")
    st.markdown("**Supported Formats:**  \n📸 PNG, JPG, JPEG")

# --- Main Content ---
st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
st.markdown("### 📤 Upload Medical Image")

file_uploaded = st.file_uploader(
    label="Choose an image file", 
    type=['png','jpg','jpeg'], 
    help="Upload a clear medical image for accurate analysis",
    label_visibility="collapsed"
)

if file_uploaded:
    st.image(file_uploaded, use_container_width=True, caption='📷 Image Preview')
    st.success("✅ Image uploaded successfully!")
    
    # File info
    file_size = len(file_uploaded.getvalue()) / 1024  # KB
    st.caption(f"📊 File size: {file_size:.1f} KB | Format: {file_uploaded.type}")
else:
    st.info("👆 Click above to upload your medical image")

st.markdown("</div>", unsafe_allow_html=True)

submit = st.button("🔍 Generate Analysis", use_container_width=True, type="primary")

# --- Analysis Section ---
st.markdown("<div class='analysis-section' style='margin-top: 20px; padding-top: 15px;'>", unsafe_allow_html=True)

analysis_placeholder = st.empty()

# --- Logic for Analysis ---
if submit:
    if not file_uploaded:
        analysis_placeholder.warning("⚠️ Please upload an image first.")
    else:
        with st.spinner("🔄 Analyzing image... Please wait"):
            try:
                image_data = file_uploaded.getvalue()
                image_parts = [{"mime_type": file_uploaded.type, "data": image_data}]
                prompt_parts = [image_parts[0], system_prompts[0]]
                
                response = model.generate_content(prompt_parts)
                
                if response and response.text:
                    # Store in session state for download
                    st.session_state.analysis_result = response.text
                    st.session_state.upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.file_name = file_uploaded.name
                    
                    # Display analysis
                    analysis_placeholder.markdown(response.text)
                    
                else:
                    analysis_placeholder.error("❌ No response generated. Please try again.")
            
            except Exception as e:
                analysis_placeholder.error(f"❌ Error generating analysis: {e}")

elif 'analysis_result' in st.session_state:
    # Display previously generated analysis
    analysis_placeholder.markdown(st.session_state.analysis_result)
else:
    analysis_placeholder.markdown("### 📊 Analysis Results")
    analysis_placeholder.info("👈 Upload an image and click 'Generate Analysis' to see results here")

st.markdown("</div>", unsafe_allow_html=True)

# --- Download Report Section ---
if 'analysis_result' in st.session_state:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Prepare report content
        report_content = f"""
VISUAL MEDICAL ASSISTANT - ANALYSIS REPORT
{'='*60}

Generated: {st.session_state.upload_time}
Image File: {st.session_state.file_name}
Analyzed by: AI Medical Assistant (Gemini 2.0 Flash)

{'='*60}

{st.session_state.analysis_result}

{'='*60}

DISCLAIMER:
This analysis is generated by an AI system and is intended for 
informational purposes only. It is NOT a substitute for professional 
medical advice, diagnosis, or treatment. Always consult with a 
qualified healthcare provider for medical decisions.

{'='*60}
Report generated by Visual Medical Assistant
Built by Md Zaheeruddin (Zaheer JK)
        """
        
        st.download_button(
            label="📥 Download Complete Report",
            data=report_content,
            file_name=f"medical_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            type="secondary"
        )
    
    with col3:
        if st.button("🗑️ Clear Analysis", use_container_width=True):
            del st.session_state.analysis_result
            del st.session_state.upload_time
            del st.session_state.file_name
            st.rerun()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); border-radius: 10px;'>
        <h4 style='color: #667eea; margin-bottom: 10px;'>⚠️ Medical Disclaimer</h4>
        <p style='color: #666; margin-bottom: 0;'>
            This AI-powered tool is designed to assist with medical image analysis but should NOT be used as a substitute 
            for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other 
            qualified health provider with any questions you may have regarding a medical condition.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999;'>Made with ❤️ by Md Zaheeruddin (Zaheer JK) | Powered by Google Gemini AI</p>", unsafe_allow_html=True)
