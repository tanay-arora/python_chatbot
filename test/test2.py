import sounddevice as sd  
import wavio as wv 
import time
import speech_recognition as sr
import wavio as wv 
import numpy as np

from playsound import playsound
from scipy.io.wavfile import write
freq = 44100
duration = 3
filename="recording.wav"

while True:
    r = sr.Recognizer()
    print("recording...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)  
    sd.wait() 
    y = (np.iinfo(np.int32).max * (recording/np.abs(recording).max())).astype(np.int32)
    #write file
    wv.write(filename, y, freq, sampwidth=2) 

    try:
        with sr.AudioFile(filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize data (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)
    except:
        print("no voice...")
        text=""
    finally:
        if "lucy" in text.lower():
            print("hey there!")
            break
        else:
            print("session completed...")