import mysql.connector
import random

mycon=mysql.connector.connect(host="localhost",user="admin",passwd="admin12345",database="chatbot")

cursor=mycon.cursor()
def get_output(keyword):
    cursor.execute('SELECT answer FROM arguments WHERE keyword="'+keyword+'";')
    data=cursor.fetchall()
    result=random.choice(data)
    return result[0]

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
