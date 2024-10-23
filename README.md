# Video Grammar Correction and Audio Replacement

This project extracts audio from a video, corrects the grammar of the speech using Azure OpenAI, converts the corrected text back to audio using Google Cloud Text-to-Speech, and reattaches the corrected audio to the original video.

## Features

- Extract audio from a video.
- Convert speech to text using Google Cloud Speech-to-Text.
- Correct grammar of the text using Azure OpenAI.
- Convert corrected text back into speech using Google Cloud Text-to-Speech.
- Replace original audio in the video with the corrected audio.

## Technologies Used

- **Python**
- **MoviePy** for handling video and audio files.
- **Google Cloud Speech-to-Text** for converting audio to text.
- **Azure OpenAI** for grammar correction.
- **Google Cloud Text-to-Speech** for converting corrected text back to speech.

## Requirements

- Python 3.x
- Google Cloud API credentials (for Speech-to-Text and Text-to-Speech)
- Azure OpenAI API credentials (for grammar correction)
- Libraries: 
  - `moviepy`
  - `requests`
  - `pydub`
  - `google-cloud-speech`
  - `google-cloud-texttospeech`
  - `dotenv`
 
## Deployment Link
  https://meet-speechresolvetask-ihgqifgt56qcutxqxbc6qj.streamlit.app/

