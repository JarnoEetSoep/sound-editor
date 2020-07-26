import tkinter as tk
from tkinter import messagebox
from subprocess import run
import os

from Application import Application

if not os.path.exists(os.path.realpath(os.path.dirname(__file__) + '/tmp')):
    os.makedirs(os.path.realpath(os.path.dirname(__file__) + '/tmp'))

root = tk.Tk()

root.resizable(1, 1)
root.attributes('-fullscreen', False)
root.minsize(850, 200)
root.geometry('950x700+50+50')

root.title('Sound Editor')

app = Application(master=root)

try:
    run('ffmpeg -loglevel quiet')
except FileNotFoundError:
    messagebox.showerror('Fatal', 'FFmpeg is not installed! Please have a look at the installation section in the docs (https://jarnoeetsoep.github.io/sound-editor/docs-page.html#introduction)')
    exit()

app.mainloop()