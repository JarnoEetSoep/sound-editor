import tkinter as tk
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

app.mainloop()