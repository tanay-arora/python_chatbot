import weathercom

from functions import filter_keywords
from output import output_voice_command
from db import get_output
from db import get_username
from db import store_name
from actions import weatherReport
from actions import input_name_data
from actions import record_user

def process_text(text,a):

    match_no=["no","nah","nhi","never","notever","not","na","naa","false"]
    match_yes=["yes","ya","yup","yeah","yeh","correct","true"]

    if "weather" in text.lower():
        weather_data=filter_keywords(text.lower(),["weather"])
        if weather_data:
            print(weather_data)
            weatherReport(weather_data)
        else:
            file_name = a.process(3)
            output_voice_command(get_output("city_name"))
            city = a.voice_command_processor(file_name)
            result = filter_keywords(city.lower(),["weather"])
            weatherReport(result)

    if "your name" in text.lower():
        output_voice_command(get_output("your_name"))
    
    if "my name" in text.lower():
        if get_username():
            file_name = a.process(3)
            output_voice_command(get_output("name_available")+" "+ get_username())
            output_voice_command(get_output("confirm_name_data"))
            response = a.voice_command_processor(file_name)
            if any(x in response.lower() for x in match_no):
                output_voice_command(get_output("ask_name"))
                input_name_data(a,match_yes,match_no)
            else:
                output_voice_command(get_output("correct"))
        else:
            output_voice_command(get_output("my_name"))
            file_name = a.process(3)
            input_name_data(a,match_yes,match_no)

    if "record" in text.lower():
        output_voice_command(get_output("recording_duration"))
        file_name = a.process(3)
        result = a.voice_command_processor(file_name)
        pre_duration = filter_keywords(result.lower(),["number","duration"])
        try:
            duration = int(pre_duration) 
            if(duration>60 or duration<0):
                duration = 10
                output_voice_command(get_output("unkown_number_default_set"))
        except:
            duration = 10 
            output_voice_command(get_output("error_voice_default_set"))
        record_user(duration)
    
    if "search" in text.lower():
        to_search = filter_keywords(text.lower(),["search"])
        