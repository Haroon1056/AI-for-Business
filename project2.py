import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

header = '''
<div class ="header">
    <p>YouTube Video Transcript Summarizer by Haroon</p>
</div>'''
youtube_link = st.text_input("Enter YouTube Video Link")

if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except IndexError:
        st.error("Invalid YouTube URL. Please enter a valid link.")

prompt = """please summarize this video transcript into 250 words or less, highlighting the key points"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([t['text'] for t in transcript_text])
        return transcript
    except Exception as e:
        return str(e)
    
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([transcript_text, prompt])
    return response.text


if st.button("Generate Summary"):
    transcripts_text = extract_transcript_details(youtube_link)
    if transcripts_text:
        summary = generate_gemini_content(transcripts_text, prompt)
        st.markdown("### Video Summary")
        st.write(summary)
