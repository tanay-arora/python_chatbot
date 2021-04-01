import random
<<<<<<< HEAD

from googletrans import Translator
import wikipedia

def google_search(search_text):
    translator = Translator()
    result = ''
    search_data = search_text
    logger.info("google_search : "+search_data)
    if "who is" in search_data or "who are" in search_data:
        search_data = search_data.split(" ")[2:]
        search_data = " ".join(search_data)
        try:
            result = wikipedia.summary(search_data, sentences=2)
        except Exception as e:
            pass
    else:
        url = "https://www.google.co.in/search?q="+search_data
        logger.info("google_search : URL : "+url)
        try:
            search_result = requests.get(url).text
            soup = BeautifulSoup(search_result, 'html.parser')

            result_div = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')

            if "born" in search_data:
                for i in result_div:
                    s = translator.translate(dest='en', text = i.text)
                    a = str(s).split("=")[3].split(",")
                    b = a[:len(a)-1]
                    b = " ".join(b)

                    if "Born" in b:
                        result = b.split(":")[1:].__str__().replace("[' ","").replace("']","")
                        #print(result)
                        break

            else:
                for i in result_div:
                    s = translator.translate(dest='en', text=i.text)
                    a = str(s).split("=")[3].split(",")
                    b = a[:len(a) - 1]
                    result = " ".join(b)
                    #print(result)
                    break
        except Exception as e:
            pass 
    logger.info("google_search : Search Result ::"+result)
    return result

print(google_search("who is narendra modi"))
=======
import sounddevice as sd  
import wavio as wv
import speech_recognition as sr
import wavio as wv 
import numpy as np
import weathercom
import json
import os

from paths import songs
from playsound import playsound
from db import get_output
from db import store_name
from db import get_username
from functions import filter_keywords
from output import output_voice_command

retry_value=2
filename = "recordings/recording2.wav"
freq = 44100

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

def next_command():
    recording(5)
    perform_actions(voice_to_text())

def user_name():
    recording(5)
    name=filter_keywords(voice_to_text(),["name"])
    confirm_name(name)

def confirm_name(name):
    output_voice_command("hey "+ name +" is it correct?")
    recording(5)
    to_match=["no","nah","nhi","never","notever","not","na","naa","false"]
    to_match_yes=["yes","ya","yup","yeah","yeh","correct","true"]
    to_check=voice_to_text().lower()
    if any(x in to_check for x in to_match):
        output_voice_command(get_output("wrong_name"))
        user_name()
    elif any(x in to_check for x in to_match_yes):
        output_voice_command(get_output("remember_name"))
        store_name(name)
        next_command()
    else:
        output_voice_command(get_output("no_voice"))
        next_command()
        
def perform_actions(text):
    music_match=["music","track","tune","song","play something"]
    if "your name" in text.lower():
        output_voice_command(get_output("your_name"))
        next_command()
    elif "my name" in text.lower():
        if get_username():
            output_voice_command(get_output("name_available")+" "+ get_username())
            output_voice_command("Is I am correct")
            recording(5)
            to_match=["no","nah","nhi","never","notever","not","na","naa","false"]
            to_match_yes=["yes","ya","yup","yeh","correct","true"]
            to_check=voice_to_text().lower()
            if any(x in to_check for x in to_match):
                user_name()   
            elif any(x in to_check for x in to_match_yes):
                output_voice_command("great")
                next_command()
            else:
                output_voice_command(get_output("no_voice"))
                next_command()
        else:
            output_voice_command(get_output("my_name"))
            user_name()
            
    elif "weather" in text.lower():
        weather_data=filter_keywords(text.lower(),["weather"])
        if weather_data:
            print(weather_data)
            weatherReport(weather_data)
        else:
            output_voice_command(get_output("weather_city_name_again"))
            recording(4)
            weather_data=filter_keywords(voice_to_text().lower(),["weather"])
            if weather_data:
                print(weather_data)
                weatherReport(weather_data)
            else:
                output_voice_command(get_output("no_voice"))

    elif "record" in text.lower():
        record_user()
        next_command()
    elif any(x in text.lower() for x in music_match):
        output_voice_command(get_output("playing_song"))
        playsound(random.choice(songs))
    elif text:
        output_voice_command(get_output("out_of_db"))
        next_command()
    else:
        global retry_value
        if retry_value>0:
            retry_value=retry_value-1
            next_command()
        else:
            retry_value=2

def record_user():
    print("...")
    output_voice_command("recording started...")
    recording = sd.rec(int(30 * freq), samplerate=freq, channels=1)  
    sd.wait() 
    y = (np.iinfo(np.int32).max * (recording/np.abs(recording).max())).astype(np.int32)
    output_voice_command("recording completed...")
    #write file
    wv.write("recordings/user_voice.falc", y, freq, sampwidth=2)
    output_voice_command("playing recording...")
    playsound("recordings/user_voice.falc")
>>>>>>> 0bb56a7f2f9b5d685cbece615a1d3b3397987f1e
