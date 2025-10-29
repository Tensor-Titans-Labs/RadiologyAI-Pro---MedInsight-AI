import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
import tempfile
from gemini_api import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Page configuration
st.set_page_config(
    page_title="RadiologyAI Pro - MedInsight AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .project-title {
        font-size: 1.2rem;
        color: #667eea;
        text-align: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #4b5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Report box styling */
    .report-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin-top: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Upload area styling */
    .uploadedFile {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Home page cards */
    .home-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 1rem;
        transition: all 0.3s ease;
    }
    
    .home-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
    }
    
    .home-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    /* Stats box */
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Disclaimer box */
    .disclaimer-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to process image
def process_image(uploaded_file):
    """Convert uploaded file to PIL Image"""
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        return None

# Helper function to generate report using Gemini
def generate_report(image, prompt):
    """Generate report using Gemini API"""
    try:
        with st.spinner("🔄 Analyzing image and generating report..."):
            response = model.generate_content([prompt, image])
            return response.text
    except Exception as e:
        st.error(f"❌ Error generating report: {str(e)}")
        return None

# Function to create PDF report
def create_pdf_report(report_text, image, report_type, patient_info=None):
    """Create a PDF report with the analysis results"""
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        story.append(Paragraph("🏥 MEDICAL IMAGING ANALYSIS REPORT", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Report Information
        story.append(Paragraph(f"<b>Report Type:</b> {report_type}", styles['Normal']))
        story.append(Paragraph(f"<b>Date Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Add patient info if provided
        if patient_info:
            story.append(Paragraph("PATIENT INFORMATION", heading_style))
            for key, value in patient_info.items():
                story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Add image if available
        if image:
            try:
                # Save image temporarily
                img_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                image.save(img_temp.name, format='PNG')
                
                # Add image to PDF
                story.append(Paragraph("ANALYZED IMAGE", heading_style))
                img = RLImage(img_temp.name, width=4*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
            except Exception as e:
                print(f"Could not add image to PDF: {e}")
        
        # Add report content
        story.append(Paragraph("ANALYSIS REPORT", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Process report text
        for line in report_text.split('\n'):
            if line.strip():
                if line.startswith('#'):
                    story.append(Paragraph(line.replace('#', '').strip(), heading_style))
                else:
                    story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Disclaimer
        story.append(Spacer(1, 0.3*inch))
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=HexColor('#dc2626'),
            borderColor=HexColor('#dc2626'),
            borderWidth=1,
            borderPadding=10,
            backColor=HexColor('#fef2f2')
        )
        story.append(Paragraph(
            "<b>⚠️ IMPORTANT DISCLAIMER:</b> This report is generated by AI and is for preliminary analysis only. "
            "All findings must be reviewed and validated by a qualified healthcare professional before making "
            "any clinical decisions.",
            disclaimer_style
        ))
        
        # Build PDF
        doc.build(story)
        
        # Read the PDF file
        with open(temp_file.name, 'rb') as f:
            pdf_data = f.read()
        
        return pdf_data
    
    except Exception as e:
        st.error(f"❌ Error creating PDF: {str(e)}")
        return None

# Navigation
st.sidebar.title("🏥 MedInsight AI")
st.sidebar.markdown("### RadiologyAI Pro")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Home", "🔍 Image Classification", "🩻 X-ray Report", "🔬 CT Scan Report", "🧠 MRI Scan Report", "🔊 Ultrasound Report"],
    label_visibility="collapsed"
)

# Extract page name without emoji
page_name = page.split(' ', 1)[1] if ' ' in page else page

# HOME PAGE
if "Home" in page:
    # Hero Section
    st.markdown('<p class="project-title">MedInsight AI Presents</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">RadiologyAI Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Diagnostic Image Analysis Platform</p>', unsafe_allow_html=True)
    
    # Introduction
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3 style="color: #667eea; text-align: center;">Welcome to the Future of Medical Imaging</h3>
        <p style="text-align: center; color: #6b7280; font-size: 1.1rem;">
        Our advanced AI-powered platform provides instant, comprehensive analysis of medical images, 
        helping healthcare professionals make faster and more informed decisions.
        </p>
        <p style="text-align: center; color: #667eea; font-weight: 600; margin-top: 1rem;">
        MedInsight AI - RadiologyAI Pro
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("### 📊 Platform Capabilities")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">5</div>
            <div class="stats-label">Imaging Modalities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">AI</div>
            <div class="stats-label">Powered Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">PDF</div>
            <div class="stats-label">Report Export</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">24/7</div>
            <div class="stats-label">Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("### 🎯 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">🔍</div>
            <h3 style="color: #667eea;">Image Classification</h3>
            <p style="color: #6b7280;">
            Automatically identify and classify medical images into X-ray, CT, MRI, or Ultrasound categories 
            with high accuracy and confidence scoring.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">🔬</div>
            <h3 style="color: #667eea;">CT Scan Analysis</h3>
            <p style="color: #6b7280;">
            Comprehensive CT scan interpretation with detailed analysis of anatomical structures, 
            densities, and potential abnormalities.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">🔊</div>
            <h3 style="color: #667eea;">Ultrasound Reports</h3>
            <p style="color: #6b7280;">
            Detailed ultrasound image analysis with measurements, echogenicity patterns, 
            and diagnostic impressions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">🩻</div>
            <h3 style="color: #667eea;">X-ray Diagnostics</h3>
            <p style="color: #6b7280;">
            Generate structured diagnostic reports from X-ray images with detailed findings, 
            impressions, and clinical recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">🧠</div>
            <h3 style="color: #667eea;">MRI Interpretation</h3>
            <p style="color: #6b7280;">
            Advanced MRI scan analysis with sequence identification, signal characteristics, 
            and detailed anatomical assessments.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">📄</div>
            <h3 style="color: #667eea;">PDF Reports</h3>
            <p style="color: #6b7280;">
            Download professionally formatted PDF reports with images, analysis results, 
            and clinical recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How it works
    st.markdown("### 🚀 How It Works")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h2 style="color: #667eea;">1️⃣</h2>
            <h4>Upload Image</h4>
            <p style="color: #6b7280;">Select and upload your medical image in supported formats</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h2 style="color: #667eea;">2️⃣</h2>
            <h4>AI Analysis</h4>
            <p style="color: #6b7280;">Our AI analyzes the image and generates comprehensive insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h2 style="color: #667eea;">3️⃣</h2>
            <h4>Get Report</h4>
            <p style="color: #6b7280;">Receive detailed analysis and download PDF report</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        <h4 style="color: #dc2626;">⚠️ Important Medical Disclaimer</h4>
        <p style="color: #991b1b;">
        This application provides AI-generated preliminary analysis for educational and research purposes only. 
        All results must be reviewed and validated by qualified healthcare professionals before making any 
        clinical decisions. This tool is not a substitute for professional medical advice, diagnosis, or treatment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h3 style="color: #667eea;">Ready to Get Started?</h3>
            <p style="color: #6b7280;">Select a feature from the navigation menu to begin your analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Team Section
    st.markdown("### 👥 Project Team")
    st.markdown("""
    <div class="feature-card">
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <th style="padding: 15px; text-align: left; border-radius: 10px 0 0 0;">Role</th>
                    <th style="padding: 15px; text-align: left; border-radius: 0 10px 0 0;">Name</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #f8f9fa;">
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;"><b>👨‍✈️ Captain</b></td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">Mohd Zaheeruddin</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;"><b>🎖️ Vice Captain</b></td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">Suman Suhan</td>
                </tr>
                <tr style="background-color: #f8f9fa;">
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;"><b>👤 Team Member</b></td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">Subiya Mahveen</td>
                </tr>
                <tr style="background-color: #ffffff;">
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;"><b>👤 Team Member</b></td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">Syed Amaan Hussani</td>
                </tr>
                <tr style="background-color: #f8f9fa;">
                    <td style="padding: 12px;"><b>👤 Team Member</b></td>
                    <td style="padding: 12px;">Humayun Attar</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# FEATURE PAGES
else:
    # Common upload and analysis interface for all features
    if "Classification" in page_name:
        st.markdown('<h1 class="main-header">🔍 Medical Image Classification</h1>', unsafe_allow_html=True)
        description = "Upload a medical image to automatically detect its type (X-ray, CT, MRI, or Ultrasound)"
        report_type = "Image Classification"
        prompt = """Analyze this medical image and classify it into one of the following categories:
        1. X-ray
        2. CT Scan
        3. MRI Scan
        4. Ultrasound
        
        Provide the classification with a confidence level and a brief explanation of the key features 
        that led to this classification. Format your response clearly with the classification type, 
        confidence percentage, and reasoning."""
        
    elif "X-ray" in page_name:
        st.markdown('<h1 class="main-header">🩻 X-ray Report Generation</h1>', unsafe_allow_html=True)
        description = "Upload an X-ray image to generate a comprehensive diagnostic report"
        report_type = "X-ray Analysis"
        prompt = """You are an expert radiologist. Analyze this X-ray image and provide a structured 
        diagnostic report including:
        
        1. **Image Quality**: Assessment of image quality and positioning
        2. **Findings**: Detailed description of anatomical structures and any abnormalities
        3. **Impression**: Summary of key findings
        4. **Recommendations**: Suggested follow-up actions or additional imaging if needed
        
        Note: Indicate that this is an AI-generated preliminary analysis and should be reviewed by 
        a qualified healthcare professional."""
        
    elif "CT Scan" in page_name:
        st.markdown('<h1 class="main-header">🔬 CT Scan Report Generation</h1>', unsafe_allow_html=True)
        description = "Upload a CT scan image to generate a detailed clinical report"
        report_type = "CT Scan Analysis"
        prompt = """You are an expert radiologist specializing in CT imaging. Analyze this CT scan 
        and provide a comprehensive clinical report including:
        
        1. **Technical Information**: Scan type, slice orientation, and contrast usage (if visible)
        2. **Anatomical Region**: Identify the body region being scanned
        3. **Findings**: Detailed analysis of visible structures, densities, and any abnormalities
        4. **Measurements**: Any relevant measurements or size assessments
        5. **Clinical Impression**: Summary interpretation
        6. **Recommendations**: Suggested follow-up or additional investigations
        
        Note: This is an AI-generated preliminary analysis requiring validation by a certified radiologist."""
        
    elif "MRI" in page_name:
        st.markdown('<h1 class="main-header">🧠 MRI Scan Report Generation</h1>', unsafe_allow_html=True)
        description = "Upload an MRI scan image to generate a comprehensive interpretation report"
        report_type = "MRI Scan Analysis"
        prompt = """You are an expert radiologist specializing in MRI imaging. Analyze this MRI scan 
        and provide a detailed interpretation report including:
        
        1. **Sequence Information**: Identify the MRI sequence type (T1, T2, FLAIR, etc.) if possible
        2. **Anatomical Region**: Specify the body region and orientation
        3. **Signal Characteristics**: Describe signal intensities and patterns
        4. **Findings**: Comprehensive analysis of structures, any lesions, or abnormalities
        5. **Differential Diagnosis**: Possible interpretations of findings
        6. **Clinical Correlation**: Recommendations for clinical correlation
        7. **Follow-up**: Suggested additional imaging or monitoring
        
        Note: This is an AI-generated preliminary analysis that must be reviewed by a qualified 
        radiologist before clinical use."""
        
    else:  # Ultrasound
        st.markdown('<h1 class="main-header">🔊 Ultrasound Report Generation</h1>', unsafe_allow_html=True)
        description = "Upload an ultrasound image to produce a diagnostic summary"
        report_type = "Ultrasound Analysis"
        prompt = """You are an expert sonographer/radiologist. Analyze this ultrasound image 
        and provide a diagnostic summary including:
        
        1. **Examination Type**: Identify the anatomical region being examined
        2. **Image Quality**: Assessment of image clarity and adequacy
        3. **Findings**: Description of visible structures, echogenicity patterns, and any abnormalities
        4. **Measurements**: Any relevant measurements (organ size, lesion dimensions, etc.)
        5. **Doppler Information**: If color Doppler is present, comment on blood flow
        6. **Impression**: Concise summary of findings
        7. **Recommendations**: Suggestions for follow-up or additional studies
        
        Note: This is an AI-generated preliminary assessment requiring confirmation by a licensed 
        healthcare professional."""
    
    st.markdown(f'<p class="sub-header">{description}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Optional patient information
    with st.expander("📋 Add Patient Information (Optional)"):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID")
            patient_age = st.text_input("Age")
        with col2:
            patient_gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
            referring_physician = st.text_input("Referring Physician")
    
    # File upload
    st.markdown("### 📤 Upload Medical Image")
    uploaded_file = st.file_uploader(
        "Choose a medical image file", 
        type=["jpg", "jpeg", "png", "dicom"],
        help="Supported formats: JPG, JPEG, PNG, DICOM"
    )
    
    if uploaded_file is not None:
        # Two column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🖼️ Uploaded Image")
            image = process_image(uploaded_file)
            if image:
                st.image(image, use_container_width=True, caption=f"Uploaded: {uploaded_file.name}")
                
                # Image info
                st.markdown(f"""
                <div class="feature-card">
                    <b>File Name:</b> {uploaded_file.name}<br>
                    <b>File Size:</b> {uploaded_file.size / 1024:.2f} KB<br>
                    <b>Image Dimensions:</b> {image.size[0]} x {image.size[1]} px
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Analysis Results")
            
            if st.button("🚀 Generate Report", use_container_width=True, type="primary"):
                result = generate_report(image, prompt)
                
                if result:
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Store in session state for download
                    st.session_state['report_text'] = result
                    st.session_state['report_image'] = image
                    st.session_state['report_type'] = report_type
                    
                    st.success("✅ Report generated successfully!")
                else:
                    st.error("❌ Failed to generate report. Please try again.")
        
        # Download section (full width below)
        if 'report_text' in st.session_state:
            st.markdown("---")
            st.markdown("### 📥 Download Report")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                # Text download
                st.download_button(
                    label="📄 Download as Text",
                    data=st.session_state['report_text'],
                    file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # PDF download
                patient_info = {}
                if patient_id:
                    patient_info["Patient ID"] = patient_id
                if patient_age:
                    patient_info["Age"] = patient_age
                if patient_gender:
                    patient_info["Gender"] = patient_gender
                if referring_physician:
                    patient_info["Referring Physician"] = referring_physician
                
                pdf_data = create_pdf_report(
                    st.session_state['report_text'],
                    st.session_state['report_image'],
                    st.session_state['report_type'],
                    patient_info if patient_info else None
                )
                
                if pdf_data:
                    st.download_button(
                        label="📑 Download as PDF",
                        data=pdf_data,
                        file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
            
            with col3:
                if st.button("🔄 Clear Results", use_container_width=True):
                    del st.session_state['report_text']
                    del st.session_state['report_image']
                    del st.session_state['report_type']
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; margin-top: 2rem;'>
        <p style='color: #6b7280; font-size: 0.9rem;'>
            <b>⚠️ Medical Disclaimer:</b> This application provides AI-generated preliminary analysis only. 
            All results must be reviewed and validated by qualified healthcare professionals before making any 
            clinical decisions.
        </p>
        <p style='color: #9ca3af; font-size: 0.8rem; margin-top: 1rem;'>
            Powered by Google Gemini AI | © 2024 MedInsight AI - RadiologyAI Pro
        </p>
    </div>
""", unsafe_allow_html=True)