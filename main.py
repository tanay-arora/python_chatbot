import sounddevice as sd  
import wavio as wv
import speech_recognition as sr
import wavio as wv 
import numpy as np

from actions import wake_greeting
from actions import perform_actions
from playsound import playsound
from output import output_voice_command
from scipy.io.wavfile import write

freq = 44100
filename="recordings/recording.wav"

def recording(duration):
    print("listening...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)  
    sd.wait() 
    y = (np.iinfo(np.int32).max * (recording/np.abs(recording).max())).astype(np.int32)
    #write file
    wv.write(filename, y, freq, sampwidth=2)

def voice_to_text():
    print("processing...")
    try:
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize data (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)
    except:
        text=""
    return text
    
def after_wakeup():
    recording(5)
    perform_actions(voice_to_text())

while True:
    recording(3)
    to_match=["hey","hii","hlo","heya","hi"]
    to_check=voice_to_text().lower()
    if any(x in to_check for x in to_match):
        wake_greeting()
        after_wakeup()
    else:
        print("...")