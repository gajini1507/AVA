import tkinter as tk
import threading
import numpy as np
import sounddevice as sd
from voice_assistant import AVA

class AVA_UI:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AVA – Accessible Virtual Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()


        self.canvas = tk.Canvas(self.root,width=300,height=100,bg="#121212")
        self.canvas.place(x=270,y=280)
        
        self.audio_data = np.zeros(1024) 

        stream = sd.InputStream(callback= self.audio_callback)
        stream.start()
        self.wave()
        

        self.title = tk.Label(
            self.root,
            text="👋 Hi, I'm AVA",
            fg="white",
            bg="#121212",
            font=("Segoe UI", 24, "bold")
        )
        self.title.pack(pady=30)
        
        self.mouse = tk.Label(
               self.root,
               text="Mouse: OFF",
               fg="#4c00ff",
               bg="#121212",
               font=("Segoe UI",14)
               
        )
        self.mouse.pack()
        self.mouse.place(x=580,y=5)

        self.status = tk.Label(
            self.root,
            text="System Initializing...",
            fg="#00ff99",
            bg="#121212",
            font=("Segoe UI", 14)
        )
        self.status.pack()

        self.lab = tk.Label(
            self.root,
            text="speak",
            bg="#121212",
            fg="#00ff99",
            font=("Segoe UI",10,"bold")
            
            )
        self.lab.place(x=350,y=200)

        self.btn = tk.Button(
        self.root,
        text="Start Listening",
        command=self.start_listen,
        bg="#00ff99",
        fg="black",
        font=("Segoe UI", 6, "bold")
             )
        self.btn.place(x=380,y=450)


    def update(self, text, color="#00ff99"):
        self.status.after(0, lambda: self.status.config(text=text, fg=color))

    def update_mouse(self, text, color="#ff5555"):
        self.status.after(0, lambda: self.mouse.config(text=text, fg=color),)

   
    def audio_callback(self, indata, frames, time, status):
        self.audio_data = np.abs(indata[:,0])

    def wave(self):
        self.canvas.delete("all")
        width = 300
        height= 100
        step = width/len(self.audio_data)

        for i,value in enumerate(self.audio_data):
            x = i*step
            y= value*100
            self.color = "cyan" if value > 0.01 else "#222222"
            self.canvas.create_line(x,height/2-y,x,height/2+y,fill="cyan")

        self.root.after(30,self.wave)

    

    def mic(self):
        self.root.after(0, lambda: self.lab.config(text="Listening..."))
        text = AVA.listen()
        self.root.after(0, lambda: self.lab.config(text=text))



    def start_listen(self):
        threading.Thread(target=self.mic,daemon=True).start()
        
    def start(self):
        self.root.mainloop()

