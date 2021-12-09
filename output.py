from gtts import gTTS
import os

def output_voice_command(text):
    language = 'en'
    speech = gTTS(text=text,lang=language,slow=False)
    speech.save("recordings/output.mp3")
    if text:
        print('... '+text)
    os.system("mpg123 -a plughw:2,0 recordings/output.mp3")
