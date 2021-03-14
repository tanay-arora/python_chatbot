import pyaudio
import wave
import speech_recognition as sr 

from wakeup import *
#File would be saved in wav format with this name
filename="record.wav"

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
print("Recording...")

for i in range(int(44100 / chunk * record_seconds)):
    data = stream.read(chunk)
    # stream.write(data)
    frames.append(data)
print("Finished recording.")
stream.stop_stream()
stream.close()

p.terminate()

#write data in file
wf = wave.open(filename,"wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(sample_rate)
wf.writeframes(b"".join(frames))
wf.close()

#convert file into text
r = sr.Recognizer()

with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize data (convert from speech to text)
    text = r.recognize_google(audio_data)
    check_wake_word(text)