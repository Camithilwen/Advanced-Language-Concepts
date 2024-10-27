#
#Import tkinter GUI libraries
#
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

#
#import author modules and declare interface
#
from webpEdit import *
interface = webpEdit()

#
#GUI configuration
#

#Frame
root = Tk()
root.title("WEBP to JPEG Converter")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, stick=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Display
filepath = StringVar()
fileDisplay = ttk.Entry(mainframe, textvariable=filepath).grid(column=3, row=1, columnspan=1)

#Buttons
def openCommand():
    #Generates tkinter file dialog and
    #passes selection to the conversion module.
    #Module passes back a keyword "OK" on success or provides
    #detail if an exception occurs.
    path = filedialog.askopenfile()
    status = interface.fileOpen(path.name)
    if status == "OK":
        pass
    else:
        messagebox.showinfo(message=status)
def convertCommand():
    #Calls conversion method and generates
    #a save dialog on completion.
    interface.fileConvert()
    #interface.fileSave(filedialog.asksavefile(mode='w'))
openButton = ttk.Button(mainframe, text="Open", command=openCommand).grid(column=3, row=3)
convertButton = ttk.Button(mainframe, text="Convert", command=convertCommand).grid(column=2, row=3)
closeButton = ttk.Button(mainframe, text="Close", command=root.quit).grid(column=4, row=3)





if __name__ == '__main__':
    #
    #Initialize GUI with above config
    #
    root.mainloop()