import tkinter as tk
from tkinter import ttk
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

    def close(self, evt: tk.Event=None):
        """Close settings window"""
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog.master.master.wm_deiconify()
    
    def show(self):
        """Open settings window"""
        self.dialog = tk.Toplevel(self.app)

        self.container = tk.Frame(self.dialog)
        self.notebook = ttk.Notebook(self.container, width=540, height=246)
        self.notebook.grid(row=0, column=0, padx=5, sticky=tk.W+tk.E+tk.N+tk.S)

        self.tab_example1 = tk.Frame(self.notebook)
        self.tab_example2 = tk.Frame(self.notebook)

        self.notebook.add(self.tab_example1, text='Example 1')
        self.notebook.add(self.tab_example2, text='Example 2')

        # Apply button
        self.cancel_apply_group = tk.Frame(self.container, width=540, height=20)
        self.cancel_button = tk.Button(self.cancel_apply_group, text='Cancel', command=self.cancel)
        self.apply_button = tk.Button(self.cancel_apply_group, text='Apply', command=self.apply)
        self.apply_and_close_button = tk.Button(self.cancel_apply_group, text='Apply and Close', command=lambda: self.apply(close=True))

        self.cancel_apply_group.grid(row=1, column=0, ipadx=3, sticky=tk.E)
        self.cancel_button.grid(row=0, column=0)
        self.apply_button.grid(row=0, column=1)
        self.apply_and_close_button.grid(row=0, column=2)

        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.dialog.grab_set()
        self.dialog.transient(self.dialog.master)
        self.dialog.title('Settings')
        self.dialog.protocol('WM_DELETE_WINDOW', self.close)

        self.dialog.wm_deiconify()
        self.dialog.geometry(f'550x300+{self.dialog.master.master.winfo_x() + self.dialog.master.master.winfo_width() // 2 - 275}+{self.dialog.master.master.winfo_y() + self.dialog.master.master.winfo_height() // 2 - 150}')
        self.dialog.resizable(0, 0)
    
    def apply(self, close: bool=False):
        """Apply changes"""
        self.config.setConfig({}).save()
        
        if close: self.close()
    
    def cancel(self):
        """Discard changes"""
        self.close()