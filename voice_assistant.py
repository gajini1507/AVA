import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import webbrowser
import subprocess
import main

class AVA:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        print("AVA:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            return self.recognizer.recognize_google(audio).lower()


    def run(self):
        self.speak("Hi, I am AVA")
        self.speak("what you want")
        while True:
            print("listening.....")
            try:
                text = self.listen()

                text = text.lower()
                if "open mouse" in text:
                       main.set_mouse_mode = True
                       self.speak("Mouse control activated")

                elif ( "sleep" or "stop" ) in text:
                            main.set_mouse_mode = False
                            self.speak("Mouse control deactivated")

                elif "search for" in text:
                     query = text.replace("search for","").strip()
                     self.speak(f"opening gooogle for {query}")
                     webbrowser.open(f"https://www.google.com/search?q={query}")

                elif "open youtube" in text:
                    self.speak("Opening YouTube")
                    webbrowser.open("https://youtube.com")

                elif "open app" in text:
                     query = text.replace("open app","").strip()
                     self.speak(f"opening app {query}")
                     subprocess.Popen(f"query".exe)
                     

                elif "open browser" in text:
                    subprocess.Popen("chrome.exe")

                elif "exit" in text: # type: ignore
                    self.speak("Goodbye")
                    break

            except:
                pass
