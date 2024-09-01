import numpy as np
from extractors import extract_audio_features, extract_text_features, extract_video_features

max_audio_length = 96
max_text_length = 28
max_video_length = 28

def video_process(video_path):
    data = []
    
    audio_features = extract_audio_features(video_path)
    text_features = extract_text_features(video_path)
    video_features = extract_video_features(video_path)
    data.append([audio_features, text_features, video_features])
    
    data = np.vstack(data)
    
    audio, text, video = video_process()
    return audio, text, video
    

def video_process():
    pass