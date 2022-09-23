import tkinter as tk
from tkinter import simpledialog as sd

root = tk.Tk()

word = sd.askstring('Word', 'What is the word?')
print(word)
print(type(word))

if not word:
    exit()

times = sd.askinteger('Times', f'How many {word}s dou you want?')
print(times)
print(type(times))

tk.Label(
    root,
    text=word*(times or 1),
    wraplength=600
).grid()

root.mainloop()
