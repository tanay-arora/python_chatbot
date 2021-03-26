import speech_recognition as sr
import pyaudio
import time
import wave
import threading
import os

from db import get_output
from output import output_voice_command

r = sr.Recognizer()

AUDIO_RATE = 44100 
AUDIO_CHANNELS = 1                
AUDIO_WIDTH = 2
AUDIO_INDEX = 0             
CHUNK = 1024
recognized_text = ''                

class voice:

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            rate=AUDIO_RATE,
            format=pyaudio.paInt16,
            channels=AUDIO_CHANNELS,
            input=True,
            frames_per_buffer=CHUNK)

    def process(self, RECORD_SECONDS):
        frames = []
        for i in range(0, int(AUDIO_RATE / CHUNK * RECORD_SECONDS)):
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        out_filename = "records/input_voice.wav"
        wf = wave.open(out_filename, 'wb')
        wf.setnchannels(AUDIO_CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.p.get_format_from_width(AUDIO_WIDTH)))
        wf.setframerate(AUDIO_RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return out_filename

    def voice_command_processor(self, filename):
        global recognized_text
        with sr.AudioFile(filename) as source:
            #r.adjust_for_ambient_noise(source=source, duration=0.5)
            wait_time = 3
            while True:
                audio = r.record(source, duration=3)
                if audio:
                    break
                time.sleep(1) #check for this time try 0 here
                wait_time = wait_time - 1
                if wait_time == 0:
                    break

            try:
                recognized_text = r.recognize_google(audio)
            except sr.UnknownValueError as e:
                pass
            except sr.RequestError as e:
                pass
            os.remove(filename)
            return recognized_text

a = voice()

if __name__ == '__main__':

    while True:
        file_name = a.process(3)
        
        print("text: " + recognized_text) #printing text check it
        if "charles" in recognized_text: #wake word here
            recognized_text = ''
            output_voice_command(get_output("wake_word"))
            time.sleep(0.5)
            command_file_name = a.process(5)
            a.voice_command_processor(command_file_name)
            #status = response.process_text(recognized_text, a) #send command from here to perform functions
            recognized_text = ''
        else:
            t1 = threading.Thread(target=a.voice_command_processor, args=(file_name,))
            t1.start()
