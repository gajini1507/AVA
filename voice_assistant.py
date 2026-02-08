import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess

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
                command = self.listen()

                
                if command is None:
                   return

                command = command.lower()
                global mouse_mode
                if "wake up" in command:
                       mouse_mode = True
                       self.speak("Mouse control activated")

                elif "sleep" in command:
                            mouse_mode = False
                            self.speak("Mouse control deactivated")

                elif "stop" in command:
                            mouse_mode = False
                            self.speak("Okay, stopping mouse mode")

                elif "search for" in command:
                     query = command.replace("search for","").strip()
                     self.speak(f"opening gooogle for {query}")
                     webbrowser.open(f"https://www.google.com/search?q={query}")

                elif "open youtube" in command:
                    self.speak("Opening YouTube")
                    webbrowser.open("https://youtube.com")

                elif "open app" in command:
                     query = command.replace("open app","").strip()
                     self.speak(f"opening app {query}")
                     subprocess.Popen(f"query".exe)
                     

                elif "open browser" in command:
                    subprocess.Popen("chrome.exe")

                elif "exit" in command:
                    self.speak("Goodbye")
                    break

            except:
                pass
