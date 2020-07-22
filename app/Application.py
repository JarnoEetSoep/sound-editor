import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import time
import os

from ConfigManager import ConfigManager

class Application(tk.Frame):
    def __init__(self, master: tk.Tk):
        """Instantiate a new application window"""
        super().__init__(master)
        self.master = master
        self.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        self.configuration = ConfigManager.load(os.path.realpath(os.path.dirname(__file__) + '/settings.json'), {'icon'})

        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.master.tk.call('wm', 'iconphoto', self.master._w, ImageTk.PhotoImage(Image.open(os.path.realpath(os.path.dirname(__file__) + '/../' + self.configuration.getConfig()['icon']))))

        self.is_fullscreen = False
        self.master.bind('<F11>', lambda e: self.fullscreen('toggle'))
        self.master.bind('<Escape>', lambda e: self.fullscreen('off'))
        
        self.createWidgets()

        self.master.update()

    def createWidgets(self):
        """Creates all widgets in the window"""
        pass
    
    def quit(self, e: tk.Event=None):
        """Kills the window and all of its subprocesses"""
        self.master.destroy()
    
    def newFile(self, e: tk.Event=None):
        """Creates a new file"""
        pass
    
    def openFile(self, e: tk.Event=None):
        """Open a sound file"""
        pass
    
    def saveFile(self, e: tk.Event=None):
        """Save the current sound file"""
        pass
    
    def saveFileAs(self, e: tk.Event=None):
        """Save the current sound file, specifying its location"""
        pass

    def openSettings(self):
        """Opens the settings dialog"""
        pass
    
    def fullscreen(self, mode):
        if mode == 'toggle':
            self.is_fullscreen = not self.is_fullscreen
            self.master.attributes('-fullscreen', self.is_fullscreen)
        elif mode == 'off':
            self.is_fullscreen = False
            self.master.attributes('-fullscreen', False)