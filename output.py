from gtts import gTTS
from playsound import playsound

def output_voice_command(text):
    language = 'en'
    speech = gTTS(text=text,lang=language,slow=False)
    speech.save("recordings/output.flac")
    if text:
        print('... '+text)
    playsound("recordings/output.flac")