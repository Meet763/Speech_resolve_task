# video_processor.py
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)
    video.close()
