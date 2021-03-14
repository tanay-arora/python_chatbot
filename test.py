import speech_recognition as sr 

filename="record.wav"

r= sr.Recognizer()

with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize data (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)