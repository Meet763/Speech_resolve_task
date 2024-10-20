import io
import os
from google.cloud import speech
from pydub import AudioSegment
import tempfile

# Use a temporary directory for file storage
temp_dir = tempfile.TemporaryDirectory()

# Set the environment variable for the Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\NODE\internshal_task - Copy\speech_to_text.json"  # Use your path here

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
