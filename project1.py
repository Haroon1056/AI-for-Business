import streamlit as st
import pathlib as pl
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

system_prompt = """
You are an advanced AI medical image analysis tool. Your task is to assist healthcare professionals in interpreting medical images and providing insights based on the visual data. You have access to a vast database of medical knowledge and imaging studies to support your analysis. Always prioritize patient safety and confidentiality in your responses."""

generation_config = {
    "temperature": 1,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain"
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
     "threshold": "BLOCK_HIGH_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
     "threshold": "BLOCK_HIGH_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
     "threshold": "BLOCK_HIGH_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
     "threshold": "BLOCK_HIGH_AND_ABOVE"}
]

#LAYOUT

st.set_page_config(page_title="Medical Image Analysis AI", layout="wide")
st.title("Medical Image Analysis AI")
upload_file = st.file_uploader("Upload a medical image", type=["png", "jpg", "jpeg"])

submit_button = st.button("Analyze Image")

if submit_button:
    image_data = upload_file.getvalue()
    
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    
    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]
    
    response = model.generate_content(prompt_parts)
    print(response.text)
    
    st.write(response.text)