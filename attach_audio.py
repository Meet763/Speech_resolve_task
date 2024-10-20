from moviepy.editor import VideoFileClip, AudioFileClip

def attach_corrected_audio_to_video(video_path, corrected_audio_path, output_video_path):
    """Attach the corrected audio to the video."""
    # Load video and corrected audio
    video_clip = VideoFileClip(video_path)
    corrected_audio = AudioFileClip(corrected_audio_path)
    
    # Set the new audio to the video
    final_video = video_clip.set_audio(corrected_audio)
    
    # Write the final video with corrected audio
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

