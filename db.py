import random
import json

file = open("./data/database.json")
data = json.load(file)
 
def get_output(key):
    for i in data["data"]:
        if i["keyword"] == key:
            result=random.choice(i["revert"])
            return result
        else:
            return "Sorry! your desired output is not in database but I will learn it soon"

def store_name(name):
    file = open("data/user_name.bin","wb")
    file.write(name)
    file.close()

def get_username():
    try:
        file = open("data/user_name.txt","r")
        return file.read()
    except:
        return ""
