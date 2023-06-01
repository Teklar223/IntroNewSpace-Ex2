import tkinter as tk
from tkinter import filedialog


def load():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile()
    return file_path

def save():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename()
    return file_path