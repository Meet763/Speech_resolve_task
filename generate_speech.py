import os
from google.cloud import texttospeech

# Set the environment variable for the Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\NODE\internshal_task - Copy\text-to-speech.json"  # Use your path here

def generate_speech(text_input, output_file="output.mp3"):
    """Generate speech from text using Google Text-to-Speech API and save it as an audio file."""
    
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the input text for synthesis
    synthesis_input = texttospeech.SynthesisInput(text=text_input)

    # Configure the voice settings (language, gender, etc.)
    voice_config = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Set the desired language
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # You can set to MALE or FEMALE as well
    )

    # Configure the audio settings (e.g., MP3 output)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # Output format as MP3
    )

    # Synthesize speech using the provided configuration
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_config,
        audio_config=audio_config
    )

    # Save the generated audio to the specified output file
    with open(output_file, "wb") as out_file:
        out_file.write(response.audio_content)
        print(f"Audio content written to '{output_file}'")

    return output_file if os.path.exists(output_file) else None