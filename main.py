import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
from dotenv import load_dotenv
import os

load_dotenv()
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")  

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")  
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")
def aiProcess(command):
    prompt = (
        "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. "
        "Give short responses please.\n\n"
        f"User: {command}"
    )

    try:
        response = model.generate_content([prompt])
        return response.text  
    except Exception as e:
        print("Gemini API Exception:", e)
        return f"Gemini Error: {e}"

  
def processCommand(c):
     if "open google" in c.lower():
          webbrowser.open("https://google.com")
     elif "open facebook" in c.lower():
          webbrowser.open("https://facebook.com")
     elif "open youtube" in c.lower():
          webbrowser.open("https://youtube.com")
     elif "open linkedin" in c.lower():
          webbrowser.open("https://linkedin.com")
     elif c.lower().startswith("play"):
          song=c.lower().split(" ")[1]
          link = musiclibrary.music[song]
          webbrowser.open(link)
     elif "news" in c.lower():
          r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
          if r.status_code == 200:
               data = r.json()
               articles = data.get('articles', [])
               
               for article in articles[:5]:
                    speak(article['title'])
          else:
               speak("Sorry, I could not fetch news right now.")

     else:
          output=aiProcess(c)
          speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=None, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))