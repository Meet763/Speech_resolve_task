import io
import os
from google.cloud import speech
from pydub import AudioSegment
import tempfile
import streamlit as st
import json

# Access the credentials from Streamlit Secrets Manager
google_credentials = st.secrets["google"]["speech_to_text_key"]

# Check if the credentials are valid JSON
try:
    credentials_dict = json.loads(google_credentials)
except json.JSONDecodeError as e:
    st.error(f"Failed to decode JSON. Please check your secrets.toml file. Error: {e}")
    raise e

# Use a temporary directory for file storage
temp_dir = tempfile.TemporaryDirectory()

# Set the desired file name
temp_file_name = "speech_to_text.json"

# Create the full path for the temp file
temp_file_path = os.path.join(temp_dir.name, temp_file_name)

# Write the credentials to the file
with open(temp_file_path, "w") as temp_file:
    temp_file.write(google_credentials)
    temp_file_path = temp_file.name
    

# Set the environment variable for the Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path  # Use your path here

def generate_text(input_file):
    """Convert audio to mono and transcribe it using Google Speech-to-Text API."""
    
    # Convert stereo audio to mono
    audio = AudioSegment.from_wav(input_file)
    mono_audio = audio.set_channels(1)  # Convert to mono
    temp_mono_audio_path = os.path.join(temp_dir.name, "temp_mono_audio.wav")
    mono_audio.export(temp_mono_audio_path, format="wav")  # Save as temporary WAV

    # Create a speech client
    client = speech.SpeechClient()

    # Read the mono audio file
    with io.open(temp_mono_audio_path, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,  # Ensure this matches your audio file's sample rate
        language_code="en-US",
        audio_channel_count=1,  # Mono audio
        enable_automatic_punctuation=True  # Adds punctuation
    )

    # Transcribe the audio file
    response = client.recognize(config=config, audio=audio)

    # Initialize an empty string to hold all the transcriptions
    full_transcription = ""

    for result in response.results:
        # Concatenate each transcript to the full_transcription string
        full_transcription += result.alternatives[0].transcript + " "  # Add a space between each transcript

    return full_transcription.strip() if full_transcription else None  # Return stripped transcription or None
