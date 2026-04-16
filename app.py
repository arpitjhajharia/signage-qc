import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup the Brain (using your secret key)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemma-4-31b-it')

st.title("🛡️ Signage QC Auditor")

# 2. Upload the 'Master' (from BOQ or Gallery)
master_file = st.file_uploader("Upload Master Artwork", type=['jpg', 'png', 'pdf'])

# 3. Capture the 'Printed' sign (iPhone Camera)
camera_file = st.camera_input("Snap photo of finished sign")

if master_file and camera_file:
    with st.spinner('Gemma 4 is auditing...'):
        master_img = Image.open(master_file)
        printed_img = Image.open(camera_file)
        
        # 4. The "Vibe" Prompt
        prompt = """
        Compare these two images for a signage factory QC process.
        Image 1: The Master Design
        Image 2: The Printed Result
        
        Check specifically for:
        1. Multilingual text errors (Arabic/Hindi/etc).
        2. Color accuracy.
        3. Missing logos or icons.
        
        Give a clear "READY FOR DISPATCH" or "REWORK REQUIRED" advisory.
        List any errors in simple bullet points.
        """
        
        response = model.generate_content([prompt, master_img, printed_img])
        
        # 5. Show the result
        if "REWORK" in response.text.upper():
            st.error(response.text)
        else:
            st.success(response.text)
