from tkinter import *
from tkinter import messagebox
import sounddevice as sound
from scipy.io.wavfile import write
import threading
import time
import numpy as np

is_recording = False
stopped_manually = False  

def start_recording():
    global is_recording
    freq = 44100
    dur = int(duration.get())
    recording = sound.rec(int(dur * freq), samplerate=freq, channels=2)
    sound.wait()
    write("recording.wav", freq, recording)
    is_recording = False
    if not stopped_manually:
        messagebox.showinfo("Recording Saved", "Recording file saved as 'recording.wav'")
    record.config(state=NORMAL)
    stop.config(state=DISABLED)
    countdown_label.config(text="")
    duration_entry.delete(0, END)

def Record():
    global is_recording
    global stopped_manually

    if is_recording:
        messagebox.showinfo("Info", "Recording is already in progress")
        return

    try:
        dur = int(duration.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the duration")
        return

    is_recording = True
    stopped_manually = False 

    record.config(state=DISABLED)
    stop.config(state=NORMAL)

    def countdown():
        for i in range(dur, -1, -1):
            if not is_recording:
                break
            countdown_label.config(text=f"{i}")
            root.update()
            time.sleep(1)
        if is_recording:
            messagebox.showinfo("Time Countdown", "Time's up")

    threading.Thread(target=start_recording).start()
    threading.Thread(target=countdown).start()

def Stop():
    global is_recording
    global stopped_manually
    
    if not is_recording:
        messagebox.showinfo("Info", "No recording in progress")
        return
    
    is_recording = False
    stopped_manually = True  
    countdown_label.config(text="")
    duration_entry.delete(0, END)

root = Tk()
root.geometry("600x800+400+10")
root.resizable(False, False)
root.title("Voice Recorder")
root.configure(background="#4a4a4a")

image_icon = PhotoImage(file="mic.png")
root.iconphoto(False, image_icon)

photo = PhotoImage(file="mic.png")
my_img = Label(image=photo, background="#4a4a4a")
my_img.pack(padx=5, pady=5)

Label(text="Voice Recorder", font="TimesNewRoman 30 bold", background="#4a4a4a", fg="white").pack()

duration = StringVar()
duration_entry = Entry(root, textvariable=duration, font="arial 30", width=15)
duration_entry.pack(pady=10)

Label(text="Enter time in seconds", font="arial 12", background="#4a4a4a", fg="white").pack()

countdown_label = Label(root, text="", font="arial 40", width=4, background="#4a4a4a", fg="white")
countdown_label.place(x=240, y=450)

record = Button(root, font="arial 20", text="Record", bg="#111111", fg="white", border=0, cursor="hand2", command=Record, activebackground="#111111")
record.place(x=150, y=700)

stop = Button(root, font="arial 20", text="Stop", bg="#111111", fg="white", border=0, cursor="hand2", command=Stop, activebackground="#111111", state=DISABLED)
stop.place(x=370, y=700)

root.mainloop()
