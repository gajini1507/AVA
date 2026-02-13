import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import webbrowser
import subprocess


class AVA:
    mouse_mode = False
    mode = "idle"

    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        self.mode = "speaking"
        print("AVA:", text)
        self.engine.say(text)
        self.engine.runAndWait()

        self.mode = "idle"

    def listen(self):
        self.mode = "listening"

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            return self.recognizer.recognize_google(audio).lower()

        self.mode = "idle"

    def run(self):
        self.speak("Hi, I am AVA")
        self.speak("what you want")
        while True:
            print("listening.....")
            try:
                text = self.listen()
                text = text.lower()
                print(f"user: {text}")

                if "power on mouse" in text:
                    self.mouse_mode = True
                    self.speak("Mouse control activated")

                elif "power of mouse" in text:
                    self.mouse_mode = False
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
                    subprocess.Popen("Google Chrome.lnk")

                elif "exit" in text: # type: ignore
                    self.speak("thank you for using")
                    break

            except:
                pass
