import tkinter as tk
import numpy as np

class AVA_UI:
    
    def __init__(self,ava):
        self.root = tk.Tk()
        self.root.title("AVA – Accessible Virtual Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.ava = ava

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

        self.canvas = tk.Label(

        )
        self.canvas.place(x=250,y=280)

       
        
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
        center_y = height // 2
        num_dots = 25
        spacing = width // num_dots


        for i in range(num_dots):
            x = i * spacing +10
            if self.ava.mode == "listening":
                y_offset = np.random.randint(-20,20)
                color = "#00ff99"

            elif self.ava.mode == "speaking":
                y_offset = np.random.randint(-30,30)
                color = "#00ff99"
            
            else:
                y_offset = 0
                color  = "#333333"

                self.canvas.create_oval(
                    x,
                    center_y + y_offset,
                    x+6,
                    center_y + y_offset + 6,
                    fill = color,
                    outline = color
                )
        self.root.after(30,self.wave)
        
    def start(self):
        self.root.mainloop()

