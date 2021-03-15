import random
import sounddevice as sd  
import wavio as wv
import speech_recognition as sr
import wavio as wv 
import numpy as np
import weathercom
import json
import os

from db import get_output
from db import store_name
from db import get_username
from functions import filter_keywords
from output import output_voice_command
from commands import wake_word
from commands import your_name
from commands import my_name
from commands import wrong_name
from commands import remember_name

filename = "recordings/recording2.wav"
freq = 44100

def wake_greeting():
    output_voice_command(get_output("wake_word"))
    
def recording(duration):
    print("listening...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)  
    sd.wait() 
    y = (np.iinfo(np.int32).max * (recording/np.abs(recording).max())).astype(np.int32)
    #write file
    wv.write(filename, y, freq, sampwidth=2)

def voice_to_text():
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
    to_match_yes=["yes","ya","yup","yeh","correct","true"]
    if any(x in voice_to_text().lower() for x in to_match):
        output_voice_command(get_output("wrong_name"))
        user_name()
    elif any(x in voice_to_text().lower() for x in to_match_yes):
        output_voice_command(get_output("remember_name"))
        store_name(name)
        next_command()

def perform_actions(text):
    if "your name" in text.lower():
        output_voice_command(get_output("your_name"))
        next_command()
    elif "my name" in text.lower():
        if get_username():
            output_voice_command(get_output("name_available"))
            output_voice_command("Is I am correct")
            recording(5)
            to_match=["no","nah","nhi","never","notever","not","na","naa","false"]
            to_match_yes=["yes","ya","yup","yeh","correct","true"]
            if any(x in voice_to_text().lower() for x in to_match):
                user_name()   
            elif any(x in voice_to_text().lower() for x in to_match_yes):
                output_voice_command("great")
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
            print('try again')
    else:
        os.system("python3 main.py")

def weatherReport(city): 
    weatherDetails = weathercom.getCityWeatherDetails(city) 
    humidity =json.loads(weatherDetails)["vt1observation"]["humidity"] 
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"] 
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    output_voice_command("It looks like "+ str(phrase) +" humitdity is "+ str(humidity) +" and temperature in " +str(city) +" is "+str(temp) )