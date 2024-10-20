import streamlit as st
from audio_transcriber import generate_text
from grammar_corrector import correct_grammar
from video_processor import extract_audio_from_video
from generate_speech import generate_speech
from attach_audio import attach_corrected_audio_to_video
import os
import tempfile


# Use a temporary directory for file storage
temp_dir = tempfile.TemporaryDirectory()

# Streamlit App
def main():
    st.title("Video to Corrected Audio with Speech Generation")

    # File uploader for video
    video_file = st.file_uploader("Upload a video file", type=["mp4"])

    # Initialize session states if not already present
    if "extracted_audio_path" not in st.session_state:
        st.session_state.extracted_audio_path = None

    if "transcription" not in st.session_state:
        st.session_state.transcription = ""
        
    if "corrected_text" not in st.session_state:
        st.session_state.corrected_text = ""

    if "audio_file_path" not in st.session_state:
        st.session_state.audio_file_path = ""

    if "output_video_path" not in st.session_state:
        st.session_state.output_video_path = ""

    # Define paths for saving the video, audio, and output files
    audio_file = os.path.join(temp_dir.name, "extracted_audio.wav")
    output_audio_file = os.path.join(temp_dir.name, "corrected_audio.wav")
    output_video_path = os.path.join(temp_dir.name, "final_output_video.mp4")

    # Step 1: Extract audio from video
    if video_file is not None:
        # Save uploaded video to the current directory
        video_path = os.path.join(temp_dir.name, "uploaded_video.mp4")
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        
        st.video(video_file)  # Display uploaded video
        
        if st.button("Extract Audio from Video"):
            with st.spinner("Extracting audio..."):
                # Extract audio from video and save to extracted_audio_path
                extract_audio_from_video(video_path, audio_file)
                st.session_state.extracted_audio_path = audio_file
                
                st.success("Audio extracted successfully!")
            
            # Display the extracted audio
            if os.path.exists(st.session_state.extracted_audio_path):
                st.audio(st.session_state.extracted_audio_path, format="audio/wav")
                st.write(f"Audio file extracted: {st.session_state.extracted_audio_path}")

    # Step 2: Transcribe audio
    if st.button("Transcribe Audio"):
        if st.session_state.extracted_audio_path:  # Check if audio has been extracted
            with st.spinner("Transcribing audio..."):
                transcription = generate_text(st.session_state.extracted_audio_path)
                st.session_state.transcription = transcription  # Save transcription to session_state
                st.text_area("Transcription", st.session_state.transcription, height=200)
        else:
            st.warning("Please extract the audio first!")

    # Step 3: Correct grammar
    if st.button("Correct Grammar"):
        if st.session_state.transcription:  # Check if transcription exists
            with st.spinner("Correcting grammar..."):
                corrected_text = correct_grammar(st.session_state.transcription)
                st.session_state.corrected_text = corrected_text  # Save corrected text
                st.text_area("Corrected Transcription", st.session_state.corrected_text, height=200)
        else:
            st.warning("Please transcribe the audio first!")

    # Step 4: Generate speech from corrected text
    if st.button("Generate Speech from Text"):
        if st.session_state.corrected_text:  # Check if corrected text exists
            with st.spinner("Generating speech..."):
                audio_file_path = generate_speech(st.session_state.corrected_text, output_audio_file)
                st.session_state.audio_file_path = audio_file_path  # Save the audio file path
                if audio_file_path:
                    st.audio(audio_file_path, format="audio/mp3")
                    st.success(f"Generated speech file saved at: {audio_file_path}")
                else:
                    st.error("Failed to generate speech.")
        else:
            st.warning("Please correct the transcription grammar first!")

    # Step 5: Attach corrected speech to original video (with wrong grammar)
    if st.button("Attach Corrected Speech to Video"):
        if st.session_state.audio_file_path and video_file and st.session_state.audio_file_path:
            with st.spinner("Attaching corrected speech to video..."):
            
                # Save the uploaded video to the current directory (if not already done)
                with open(video_path, "wb") as f:
                    f.write(video_file.read())
            
                # Path for the output video with corrected speech
                output_video_path_with_speech = os.path.join(temp_dir.name, "video_with_speech.mp4")
            
                # Now attach the generated speech audio to the original video (with the wrong grammar)
                attach_corrected_audio_to_video(video_path, st.session_state.audio_file_path, output_video_path_with_speech)
            
                # Update session state with the output video path
                st.session_state.output_video_path = output_video_path_with_speech
            
                # Success message
                st.success(f"Video with corrected speech attached saved at: {output_video_path_with_speech}")
                
                # Display final video
                if os.path.exists(output_video_path_with_speech):
                    st.video(output_video_path_with_speech)
        else:
            st.warning("Please generate speech and upload a video file first!")


# Run the Streamlit app
if __name__ == "__main__":
    main()
