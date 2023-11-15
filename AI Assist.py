import pyttsx3
from datetime import datetime
import speech_recognition as sr
import wikipedia as wk
import webbrowser as wb
import os
import subprocess as sp
import requests
import json
#import smtplib
import requests
from pprint import pprint
from urllib.request import urlopen
import urllib.parse
#from bs4 import BeautifulSoup



paths = {
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

engine = pyttsx3.init('sapi5')

voices= engine.getProperty('voices') #getting details of current voice
print(voices[1].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio) 
    engine.runAndWait() #Without this command, speech will not be audible to us.

def wishme():
    hour=int(datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good morning!")
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        print("Good Afternoon!")
        speak("Good Afternoon!")
    else:
        print("Good Evening!")
        speak("Good Evening!")

   # print("How may I help you?")
    speak("How may I help you?")    
    speak("These are the services provided by AI Desktop Assistant")
    print("SERVICES:")
    print("1.Check time")
    print("2.Open calculator")
    print("3.Open Google")
    print("4.Open Wikipedia")
    print("5.Listen to music")
    print("6.Check the latest news")
    print("7.Open camera")
    print("8.Check the weather")


def speak_news():
    url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=ba1f42b5a6974533a4355cd879017c8a'
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict[news]
    speak('Source: The Times Of India')
    speak('Todays Headlines are..')
    for index,article in enumerate(arts):
        speak(article['title'])
        if index == len(arts)-1:
            break
        speak('Moving on the next news headline..')
    speak('These were the top headlines, Have a nice day!!..')


def get_weather_report(city):
    res = requests.get()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


def takeCommand():
    #It takes microphone input from the user and returns string output
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 0.8
        r.energy_threshold = 1000
        r.adjust_for_ambient_noise(source, duration=3)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    
    except Exception as e:
        print(e)

        print("Say that again please...")
        return "None"    
    return query



if __name__=="__main__" :
    #speak("Hey Payel")
    wishme()
    while True:
        query=takeCommand().lower()

    #Executing tasks
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia"," ")
            results = wk.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)



        elif 'open youtube' in query:
            r1=sr.Recognizer() 
            url="https://www.youtube.com/results?search_query="
            with sr.Microphone() as source:
                speak("What video do you want to search?")
                audio=r1.listen(source)
            try:
                get=r1.recognize_google(audio)
                print(get)
                wb.get().open_new(url+get)
            except sr.UnknownValueError:
                print("error")
            except sr.RequestError as e:
                print('failed'.format(e))
            except:
                print("No Microphone Detected")
            

        
        elif 'open google' in query:
            r2=sr.Recognizer()
            url="https://www.google.co.in/search?q="
            with sr.Microphone() as source:
                speak("What do you want to search?")
                audio=r2.listen(source)
            try:
                get=r2.recognize_google(audio)
                print(get)
                wb.get().open_new(url+get)
            except sr.UnknownValueError:
                print("error")
            except sr.RequestError as e:
                print('failed'.format(e))
            except:
                print("Microphone not detected")  
            

        elif 'music' in query:
            music_dir= 'D:\\Roadtrack'    
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))
        
        elif 'time' in query:
            strTime=datetime.now().strftime("%H:%M:%S")
            print(f"The time is {strTime}")
            speak(f"The time is {strTime}")
        
        

        elif 'calculator' in query:
            sp.Popen(paths['calculator'])

        elif 'command promt' in query:
            os.startfile(os.path['command promt'])
        
        elif 'news' in query:
            speak("These are the latest news headlines!")
            url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=ba1f42b5a6974533a4355cd879017c8a'
            news = requests.get(url).text
            news_dict = json.loads(news)
            arts = news_dict[news]
            speak('Source: The Times Of India')
            speak('Todays Headlines are..')
            for index,article in enumerate(arts):
                speak(article['title'])
                if index == len(arts)-1:
                    break
                speak('Moving on the next news headline..')
                speak('These were the top headlines, Have a nice day!!..')
        
            speak("For your convenience, I am printing it on the screen sir.")
            print(*speak_news(), sep='\n')
        
        elif 'weather' in query:
            api_key = "bd31648e8417e58465fd929e6f1da172"
            city='New Delhi'
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(base_url)
            data = json.loads(response.text)
            if data["cod"] == "404":
                print("City not found.")
            else:
                main_info = data["weather"][0]["main"]
                description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                speak(f"Weather in {city}: {main_info}, {description}")
                speak(f"Temperature: {temperature}K")
                speak(f"Humidity: {humidity}%")
                print(f"Weather in {city}: {main_info}, {description}")
                print(f"Temperature: {temperature}K")
                print(f"Humidity: {humidity}%")
            

        elif 'camera' in query:
             sp.run('start microsoft.windows.camera:', shell=True)
