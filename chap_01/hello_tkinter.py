"""Hello World application for Tkinter"""
import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="Hello World!")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Presioname")
button.pack()

root.mainloop()
