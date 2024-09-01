from moviepy.editor import VideoFileClip
import os
import cv2
import dlib
import pytesseract
import librosa

# Function to extract audio features from a video
def extract_audio_features(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio_path = 'temp_audio.wav'
    audio.write_audiofile(audio_path)

    audio_data, sample_rate = librosa.load(audio_path)
    audio_features = librosa.feature.mfcc(y=audio_data, sr=sample_rate)

    os.remove(audio_path)

    return audio_features

# Function to extract text features from a video
def extract_text_features(video_path):
    video = VideoFileClip(video_path)
    frames = video.iter_frames()

    text = ""
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_text = pytesseract.image_to_string(gray)
        text += frame_text

    return text

# Function to extract video features from a video
def extract_video_features(video_path):
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor = dlib.shape_predictor('/home/aikumis/shape_predictor_68_face_landmarks.dat')

    video_capture = cv2.VideoCapture(video_path)
    video_features = []

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray)

        for face in faces:
            landmarks = landmark_predictor(gray, face)
            landmark_coordinates = [(landmark.x, landmark.y) for landmark in landmarks.parts()]
            video_features.append(landmark_coordinates)

    video_capture.release()

    return video_features