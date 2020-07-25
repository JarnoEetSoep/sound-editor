import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser
from scipy.io import wavfile
import numpy as np
import json
import time
import os

from ConfigManager import ConfigManager
from SettingsDialog import SettingsDialog
import Exceptions as e

ExpectedConfigKeys = {'icon','lang','supported_extensions'}

class Application(tk.Frame):
    """Application window"""
    def __init__(self, master: tk.Tk):
        """Instantiate a new application window"""
        super().__init__(master)
        self.master = master
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.configuration = ConfigManager.load(os.path.realpath(os.path.dirname(__file__) + '/settings.json'), ExpectedConfigKeys)
        self.settings_dialog = SettingsDialog(self, self.configuration) 

        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.master.tk.call('wm', 'iconphoto', self.master._w, ImageTk.PhotoImage(Image.open(os.path.realpath(os.path.dirname(__file__) + '/../' + self.configuration.getConfig()['icon']))))

        self.is_fullscreen = False
        self.master.bind('<F11>', lambda e: self.fullscreen('toggle'))
        self.master.bind('<Escape>', lambda e: self.fullscreen('off'))
        
        self.current_file = {}
        self.file = None
        self.progress = False

        self.createWidgets()

        self.master.update()

    def createWidgets(self):
        """Creates all widgets in the window"""
        # Top menu
        self.menu = tk.Menu(self.master)
        self.menu_file = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.menu_file)

        self.menu_file.add_command(label='New File', accelerator='Ctrl+N', command=self.newFile)
        self.master.bind_all('<Control-n>', self.newFile)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Open File...', accelerator='Ctrl+O', command=self.openFile)
        self.master.bind_all('<Control-o>', self.openFile)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Save File', accelerator='Ctrl+S', command=self.saveFile)
        self.master.bind_all('<Control-s>', self.saveFile)
        self.menu_file.add_command(label='Save File As...', accelerator='Ctrl+Shift+S', command=self.saveFileAs)
        self.master.bind_all('<Control-S>', self.saveFileAs)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Settings', accelerator='Ctrl+,', command=self.openSettings)
        self.master.bind_all('<Control-comma>', self.openSettings)

        self.menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)

        self.menu_edit.add_command(label='Undo', accelerator='Ctrl+Z', command=self.undo)
        self.master.bind_all('<Control-z>', self.help)
        self.menu_edit.add_command(label='Redo', accelerator='Ctrl+Y', command=self.redo)
        self.master.bind_all('<Control-y>', self.help)
        
        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Help', menu=self.menu_help)

        self.menu_help.add_command(label='Manual', accelerator='F1', command=self.help)
        self.master.bind_all('<F1>', self.help)

        self.master.config(menu=self.menu)
    
    def quit(self, evt: tk.Event=None):
        """Kills the window and all of its subprocesses"""
        if self.progress:
            if not messagebox.askokcancel(self.configuration.getLang()['discardChanges']['title'], self.configuration.getLang()['discardChanges']['message']):
                return

        if os.path.exists(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav')):
            os.remove(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav'))

        self.master.destroy()
    
    def newFile(self, evt: tk.Event=None):
        """Creates a new file"""
        proceed = messagebox.askokcancel(self.configuration.getLang()['discardChanges']['title'], self.configuration.getLang()['discardChanges']['message']) if self.progress else True
        if not proceed: return
        
        if os.path.exists(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav')):
            os.remove(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav'))
        
        self.current_file = {}
        self.master.wm_title('Sound Editor')

    def openFile(self, evt: tk.Event=None):
        """Open a sound file"""
        proceed = messagebox.askokcancel(self.configuration.getLang()['discardChanges']['title'], self.configuration.getLang()['discardChanges']['message']) if self.progress else True
        if not proceed: return

        path = filedialog.askopenfilename(initialdir=os.path.expanduser('~'), title='Open Sound File', filetypes=[('Sound files', ' '.join(self.configuration.getConfig()['supported_extensions']))])

        if path:
            path = os.path.realpath(path)
            self.current_file['path'] = path

            if os.path.exists(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav')):
                os.remove(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav'))

            os.system(f'ffmpeg -y -loglevel quiet -i {path} {os.path.realpath(os.path.dirname(__file__) + "/data/current.wav")}')

            try:
                self.current_file['rate'], self.current_file['data'] = wavfile.read(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav'))
            except FileNotFoundError:
                self.current_file = {}
                print('Sound file is corrupt or could not be opened')
                raise
            except ValueError:
                self.current_file = {}
                print('Sound file is corrupt')
                raise
            else:
                self.master.wm_title(f'Sound Editor - {os.path.basename(path)}')
                self.progress = False
    
    def saveFile(self, evt: tk.Event=None):
        """Save the current sound file"""
        if 'path' in self.current_file.keys():
            wavfile.write(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav'), self.current_file['rate'], self.current_file['data'])

            savestate = os.system(f'ffmpeg -y -loglevel quiet -i {os.path.realpath(os.path.dirname(__file__) + "/data/current.wav")} {self.current_file["path"]}')
            if savestate == 1:
                raise e.SaveFileError
                
            self.master.wm_title(f'Sound Editor - {os.path.basename(self.current_file["path"])}')
            self.progress = False
        else:
            self.saveFileAs()
    
    def saveFileAs(self, e: tk.Event=None):
        """Save the current sound file, specifying its location"""
        path = filedialog.asksaveasfilename(initialdir=os.path.expanduser('~'), title='Save Sound File', filetypes=[('Sound files', ' '.join(self.configuration.getConfig()['supported_extensions']))])
        
        if path:
            valid_extension = []
            for ext in self.configuration.getConfig()['supported_extensions']:
                valid_extension.append(path.endswith(ext))

            if not True in valid_extension: path += '.mp3'

            self.current_file['path'] = path

            if not 'data' in self.current_file:
                self.current_file['rate'] = 44100
                self.current_file['data'] = np.array([[0, 0]] * 1)

            wavfile.write(os.path.realpath(os.path.dirname(__file__) + '/data/current.wav'), self.current_file['rate'], self.current_file['data'])
            savestate = os.system(f'ffmpeg -y -loglevel quiet -i {os.path.realpath(os.path.dirname(__file__) + "/data/current.wav")} {self.current_file["path"]}')

            if savestate == 1:
                raise e.SaveFileError
                
            self.master.wm_title(f'Sound Editor - {os.path.basename(path)}')
            self.progress = False

    def openSettings(self, evt: tk.Event=None):
        """Opens the settings dialog"""
        if not self.settings_dialog.isVisible:
            self.settings_dialog.show()
    
    def help(self, evt: tk.Event=None):
        """Opens the manual"""
        webbrowser.open_new('file:///' + os.path.realpath(os.path.join(os.path.dirname(__file__), '../docs/docs-page.html')))

    def undo(self, evt: tk.Event=None):
        """Undoes last action"""
        pass

    def redo(self, evt: tk.Event=None):
        """Redoes last undone action"""
        pass

    def fullscreen(self, mode):
        """Toggle fullscreen, or windowify (when pressing Esc)"""
        if mode == 'toggle':
            self.is_fullscreen = not self.is_fullscreen
            self.master.attributes('-fullscreen', self.is_fullscreen)
        elif mode == 'off':
            self.is_fullscreen = False
            self.master.attributes('-fullscreen', False)