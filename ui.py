import tkinter as tk

class AVA_UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AVA – Accessible Virtual Assistant")
        self.root.geometry("500x300")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.title = tk.Label(
            self.root,
            text="👋 Hi, I'm AVA",
            fg="white",
            bg="#121212",
            font=("Segoe UI", 24, "bold")
        )
        self.title.pack(pady=30)

        self.status = tk.Label(
            self.root,
            text="System Initializing...",
            fg="#00ff99",
            bg="#121212",
            font=("Segoe UI", 14)
        )
        self.status.pack()

    def update(self, text, color="#00ff99"):
        self.status.after(0, lambda: self.status.config(text=text, fg=color))

    def start(self):
        self.root.mainloop()
