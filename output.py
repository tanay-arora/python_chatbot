from gtts import gTTS
import os

def output_voice_command(text):
    language = 'en'
    speech = gTTS(text=text,lang=language,slow=False)
    speech.save("test_text.mp3")
    os.system("mpg321 test_text.mp3")