from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", return_timestamps=True)

def transcribe_audio(file_path):
    """ uses the openai/whisper-large-v3 model to transcribe the audio file """
    result = pipe(file_path)
    return result["text"]