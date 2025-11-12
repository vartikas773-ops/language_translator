import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
from playsound import playsound
import pyperclip
import threading
import time
import webbrowser

def watch_clipboard():
    global last_clipboard
    while True:
        try:
            current = pyperclip.paste()
            if current != last_clipboard and len(current.strip()) > 0:
                last_clipboard = current
                input_text.delete("1.0", tk.END)
                input_text.insert(tk.END, current)
        except Exception:
            pass
        time.sleep(1.5)  # Check every 1.5 seconds

translator = Translator()
translation_history = []
last_clipboard = ""

root = tk.Tk()
root.title("Language Translator")
root.geometry("700x600")
root.configure(bg="#fcefee")

style = ttk.Style()
style.configure("TLabel", background="#fcefee", font=("Helvetica", 18))
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TCombobox", padding=5)

frame = tk.Frame(root, bg="#f9d5e5", bd=4, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=530)

top_frame = tk.Frame(frame, bg="#f9d5e5")
top_frame.pack(pady=10)

lang_label = ttk.Label(top_frame, text="Translate to:")
lang_label.pack(side="left", padx=(0, 10))

lang_var = tk.StringVar()
lang_combo = ttk.Combobox(top_frame, textvariable=lang_var, state="readonly", width=30)
lang_combo['values'] = list(LANGUAGES.values())
lang_combo.set("french")
lang_combo.pack(side="left")

text_frame = tk.Frame(frame, bg="#f9d5e5")
text_frame.pack(pady=10)

input_box = tk.Frame(text_frame, bg="#f9d5e5")
input_box.pack(side="left", padx=10)

input_label = ttk.Label(input_box, text="Enter text:")
input_label.pack()
input_text = tk.Text(input_box, height=17, width=30, wrap="word", font=("Helvetica", 11))
input_text.pack()

output_box = tk.Frame(text_frame, bg="#f9d5e5")
output_box.pack(side="left", padx=10)

output_label = ttk.Label(output_box, text="Translated text:")
output_label.pack()
output_text = tk.Text(output_box, height=17, width=30, wrap="word", font=("Helvetica", 11), bg="#fff0f5")
output_text.pack()

def translate_text():
    try:
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to translate.")
            return
        dest_lang = lang_var.get()
        lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(dest_lang)]
        translated = translator.translate(text, dest=lang_code)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)

        history_entry = f"[{dest_lang.title()}] {text} → {translated.text}"
        translation_history.append(history_entry)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def speak_text():
    try:
        text = output_text.get("1.0", tk.END).strip()
        if text:
            tts = gTTS(text=text, lang='en')
            tts.save("temp.mp3")
            playsound("temp.mp3")
            os.remove("temp.mp3")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def speech_to_text():
    messagebox.showinfo("Info", "Copy your spoken text from Dictation.io — it will auto-paste here.")

def watch_clipboard():
    global last_clipboard
    while True:
        try:
            current = pyperclip.paste()
            if current != last_clipboard and len(current.strip()) > 0:
                last_clipboard = current
                input_text.delete("1.0", tk.END)
                input_text.insert(tk.END, current)
        except Exception:
            pass
        time.sleep(1.5)

def open_speech_tool():
    try:
        webbrowser.open("https://dictation.io/speech")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open browser: {e}")

def show_history():
    history_win = tk.Toplevel(root)
    history_win.title("Translation History")
    history_win.geometry("400x300")
    history_win.configure(bg="#fcefee")

    hist_frame = tk.Frame(history_win, bg="#f9d5e5", bd=3, relief="groove")
    hist_frame.pack(padx=10, pady=10, fill="both", expand=True)

    hist_label = ttk.Label(hist_frame, text="Past Translations:")
    hist_label.pack(pady=5)

    hist_text = tk.Text(hist_frame, height=10, wrap="word", font=("Helvetica", 11), bg="#fff0f5")
    hist_text.pack(padx=10, pady=5, fill="both", expand=True)

    for item in translation_history:
        hist_text.insert(tk.END, item + "\n")

    def clear_history():
        translation_history.clear()
        hist_text.delete("1.0", tk.END)

    button_row = tk.Frame(hist_frame, bg="#f9d5e5")
    button_row.pack(pady=10)

    clear_btn2 = ttk.Button(button_row, text="Clear", command=clear_history)
    clear_btn2.pack(side="left", padx=10)


button_frame = tk.Frame(frame, bg="#f9d5e5")
button_frame.pack(pady=10)

translate_btn = ttk.Button(button_frame, text="Translate", command=translate_text)
translate_btn.grid(row=0, column=0, padx=10)

speak_btn = ttk.Button(button_frame, text="Speak", command=speak_text)
speak_btn.grid(row=0, column=1, padx=10)

history_btn = ttk.Button(button_frame, text="History", command=show_history)
history_btn.grid(row=0, column=2, padx=10)

open_tool_btn = ttk.Button(button_frame, text="Open Speech Tool", command=open_speech_tool)
open_tool_btn.grid(row=0, column=3, padx=10)

threading.Thread(target=watch_clipboard, daemon=True).start()
def on_close():
    try:
        pyperclip.copy("")  # Clear clipboard
    except Exception:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()