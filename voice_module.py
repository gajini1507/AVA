import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import os

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_and_execute(self):
        with sr.Microphone() as source:
            try:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"User: {text}")


                if "search for" in text:
                    query = text.replace("search for", "").strip()
                    self.speak(f"Searching for {query}")
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                
                elif "open the" in text:
                    query = text.replace("open the","").strip()
                    self.speak(f"Open the {query}")  
                    subprocess.Popen(f"{query}.exe")


                elif "open browser" in text:
                    self.speak("Opening Chrome")
                    # Update this path if your Chrome is installed elsewhere
                    subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


            except Exception as e:
                pass