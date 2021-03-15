import pyaudio
import wave
import speech_recognition as sr 
import time
import os

r = sr.Recognizer()
filename="recording.wav"

chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
record_seconds = 5

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
    channels=channels,
    rate=sample_rate,
    input=True,
    output=True,
    frames_per_buffer=chunk)

frames = []
for i in range(0,int(44100 / chunk * record_seconds)):
    data = stream.read(chunk,exception_on_overflow=False)
    # stream.write(data)
    frames.append(data)
    
#write data in file
wf = wave.open(filename,"wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(sample_rate)
wf.writeframes(b"".join(frames))
wf.close()