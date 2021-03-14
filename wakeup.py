import re
def check_wake_word(text):
    print(text)
    if "charles" in text.lower():
        print("hey there!")
check_wake_word("hey charles")