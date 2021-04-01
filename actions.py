import weathercom
import json
import wavio as wv
import numpy as np
import sounddevice as sd

from playsound import playsound
from functions import filter_keywords
from db import get_output
from db import store_name
from output import output_voice_command

def weatherReport(city): 
    try:
        weatherDetails = weathercom.getCityWeatherDetails(city) 
        humidity =json.loads(weatherDetails)["vt1observation"]["humidity"] 
        temp = json.loads(weatherDetails)["vt1observation"]["temperature"] 
        phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
        output_voice_command("It looks like "+ str(phrase) +". humidity is "+ str(humidity) +" percent and temperature in " +str(city) +" is "+str(temp)+" degree celcius" )
    except:
        output_voice_command(get_output("no_location"))

def input_name_data(a,match_yes,match_no):
    file_name = a.process(3)
    name_resp = a.voice_command_processor(file_name)
    name = filter_keywords(name_resp,["name"])
    output_voice_command(get_output("confirm_name_data"))
    write_in_confirm = a.voice_command_processor(file_name)
    if any(x in write_in_confirm.lower() for x in match_yes ):
        store_name(name)
        output_voice_command(get_output("remember_name")+" "+name)
    else:
        output_voice_command(get_output("no_voice"))

def record_user(duration):
    freq = 44100
    print("...")
    output_voice_command("recording started...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)  
    sd.wait() 
    y = (np.iinfo(np.int32).max * (recording/np.abs(recording).max())).astype(np.int32)
    output_voice_command("recording completed...")
    
    wv.write("recordings/user_voice.falc", y, freq, sampwidth=2)
    output_voice_command("playing recording...")
    playsound("recordings/user_voice.falc")