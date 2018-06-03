import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
import re
import wikipedia
import webbrowser
from weather import Weather
import json
import requests
weather=Weather()
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 -q audio.mp3")
    os.remove("audio.mp3")
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data.lower()
    
def jarvis(data):
	if "how are you" in data:
		speak("I am fine")
	
	if "what time is it" in data:
		speak(ctime())
	
	if "where is" in data:
		data=data.split(" ")
		location=data[2]
		speak("Hold on Frank, I will show you where" + location + "is.")
		os.system("firefox https://www.google.nl/maps/place/" + location)
	
	if "search wikipedia" in data:
		data=data.split(" ")
		value=data[2:]
		speak("Hold on Frank, I will show you ")
		speak(wikipedia.summary(value,sentences=2))
		
	if "search images of" in data:
		data=data.split(" ")
		value=data[3:]
		#speak("Hold on Frank, I will show you "  + value +  " is." )
		url="https://www.google.co.in/search?q={}&tbm=isch".format(value)
		webbrowser.open_new_tab(url)
	
	if "search google" in data:
		data=data.split(" ")
		value=data[2:]
		#speak("Hold on Frank, I will show you "  + value +  " is." )
		url="https://www.google.co.in/search?q={}".format(value)
		webbrowser.open_new_tab(url)
	
	
	if "weather forecast in " in data:
		data=data.split(" ")
		value=data[3]
		location = weather.lookup_by_location(value)
		forecasts = location.forecast()
		for forecast in forecasts:
			speak(forecast.text())
			speak(forecast.date())
			speak(forecast.high())
			speak(forecast.low())
			
	if "search word " in data:
		app_id = '403a4169'
		app_key = '7702e3891078f4285fd0a043052eac84'
		language = 'en'
		data=data.split(" ")
		value=data[2]
		url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' +  value
		req = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})	
		dump = req.json()
		dump=dump['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
		speak("Meaning: " +dump)
		
		
			
	if "bye bye jarvis" in data:
		speak("Bye Bye!!")
		exit(0)
		
    		
	
		
		
	
		
		
#intialization
time.sleep(2)
speak("Hi Frank, what can I do for you?")
while(True):
	data=recordAudio()
	jarvis(data)
