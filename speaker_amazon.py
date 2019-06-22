
import json
import time
import os
from gtts import gTTS
import botbase
import requests
import platform
import pygame
pygame.mixer.init()

QUIT = False

file = open("token.txt")
TOKEN = file.read().strip()
file.close()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
BOT = botbase.BotBase(URL)

###############################
# Button options and commands #
###############################

lo = ["Turn on", "Turn off"]
lights = {"Nick": lo, "Guest": lo, "Lamp": lo, "Master": lo}

tivo = ["Pause", "Play", "Fast Forward", "Previous", "Skip", "Go to Guide", "Go to Home", "Go to Settings"]
tv_options = {"Display", "Hulu", ""}

options = {"Lights": lights, "T.V.":tv_options} # base menu

############################
# Type of response methods #
############################

def is_button_response(update):
    try:
        update['callback_query']
    except Exception:
        return False
    return True

def is_message_with_text(update):
    try:
        update['message']['text']
    except Exception:
        return False
    return True

def read(update):
    try:
        print(update)
        message = update["message"]
        text = message['text']
        if "/on" in text:
            speak("Amazon turn on nick")
        elif "off" in text:
            speak("Amazon turn off nick")
        elif str(update["user"]["id"]) == "569239019":
            speak("Amazon {}".format(text))
    except Exception as e:
        print(e)
        return
#         raise(e)

def speak(toread):
    myobj = gTTS(text = toread, lang='en', slow=False)
    myobj.save("toplay.mp3")
    if platform.system() == "Darwin": #detects macos 
   	 os.system("afplay toplay.mp3")
    else:
         print(toread)
         pygame.mixer.music.load("toplay.mp3")
         pygame.mixer.music.play() 
         print("played")

def main():
    last_update_id = None
    while True:
        updates = BOT.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = BOT.get_last_update_id(updates) + 1
            print(updates)
            for update in updates["result"]:
                read(update)
        time.sleep(0.5)

if __name__ == '__main__':
    main()  
