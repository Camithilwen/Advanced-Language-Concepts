from tkinter import *
from tkinter import ttk
from tkinter import filedialog

root = Tk()
root.title("WEBP to JPEG Converter")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, stick=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#inputFile = filedialog.askopenfilename()
root.mainloop()