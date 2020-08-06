import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

from ConfigManager import ConfigManager

class SettingsDialog:
    """Dialog for changing the settings"""
    def __init__(self, master: tk.Tk, config: ConfigManager):
        """Configure a new settings window"""
        self.app = master
        self.config = config
        self.changes = False
        self.isVisible = False

        self.languages = {
            'English': 'assets/lang/en-us.json',
            'Nederlands': 'assets/lang/nl-nl.json'
        }

    def close(self, evt: tk.Event=None):
        """Close settings window"""
        self.isVisible = False
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog.master.master.wm_deiconify()
    
    def show(self):
        """Open settings window"""
        self.isVisible = True
        self.dialog = tk.Toplevel(self.app)
        self.container = tk.Frame(self.dialog)
        
        self.container.bind('<Configure>', self.resize)

        self.style = ttk.Style(self.container)
        self.style.configure('.', font=('verdana', 10))
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self.style.layout('Tab', [('Notebook.tab', {'sticky': 'nswe', 'children': [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [('Notebook.label', {'side': 'top', 'sticky': ''})]})]})])
        self.dialog.option_add('*TCombobox*Listbox.font', ('verdana', 10))

        self.notebook = ttk.Notebook(self.container, style='lefttab.TNotebook')
        self.notebook.pack(fill=tk.X, expand=1, anchor=tk.N)

        self.tab_preferences = tk.Frame(self.notebook)

        self.notebook.add(self.tab_preferences, text=self.config.getLang()['settings']['preferences'])

        # Preferences tab
        self.language_label = tk.Label(self.tab_preferences, text=self.config.getLang()['settings']['languagelabel'], font=('Verdana', 10))

        langs = ['English', 'Nederlands']
        self.language_input = ttk.Combobox(self.tab_preferences, values=langs, font=('Verdana', 10), state='readonly')
        self.language_input.current(langs.index({path: lang for lang, path in self.languages.items()}[self.config.getConfig()['lang']]))

        self.language_label.grid(row = 0, column = 0)
        self.language_input.grid(row = 0, column = 1)

        # Apply button
        self.cancel_apply_group = tk.Frame(self.container)
        self.cancel_button = ttk.Button(self.cancel_apply_group, text=self.config.getLang()['settings']['cancel'], command=self.cancel)
        self.apply_button = ttk.Button(self.cancel_apply_group, text=self.config.getLang()['settings']['apply'], command=self.apply)
        self.apply_and_close_button = ttk.Button(self.cancel_apply_group, text=self.config.getLang()['settings']['applyandclose'], command=lambda: self.apply(close=True))

        self.cancel_apply_group.pack(fill=tk.Y, expand=1, anchor=tk.E)
        self.cancel_button.grid(row=0, column=0)
        self.apply_button.grid(row=0, column=1)
        self.apply_and_close_button.grid(row=0, column=2)

        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.dialog.grab_set()
        self.dialog.focus_set()
        self.dialog.transient(self.dialog.master)
        self.dialog.title(self.config.getLang()['settings']['title'])
        self.dialog.protocol('WM_DELETE_WINDOW', self.cancel)

        self.dialog.wm_deiconify()
        self.dialog.geometry(f'550x300+{self.dialog.master.master.winfo_x() + self.dialog.master.master.winfo_width() // 2 - 275}+{self.dialog.master.master.winfo_y() + self.dialog.master.master.winfo_height() // 2 - 150}')
    
    def apply(self, close: bool=False):
        """Apply changes"""
        newConfig = self.config.getConfig()

        newConfig['lang'] = self.languages[self.language_input.get()]

        self.config.setConfig(newConfig).save()
        
        if close: self.close()
    
    def cancel(self):
        """Discard changes"""
        if self.changes:
            if messagebox.askokcancel(self.config.getLang()['discardChanges']['title'], self.config.getLang()['discardChanges']['message']):
                self.close()
        else:
            self.close()
    
    def resize(self, evt: tk.Event):
        """Called when the window is being resized"""
        self.notebook.configure(height=evt.height-30)