#
#Import tkinter GUI libraries
#
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
#
#import author modules and declare interface
#
from WEBPconvert import *
interface = WEBPconvert()

#
#GUI configuration
#

#Frame
root = Tk()
root.title("WEBP to PNG Converter")
root.geometry("300x200")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, stick=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Display
filepath = StringVar()
fileDisplay = ttk.Entry(mainframe, textvariable=filepath, width=80)
fileDisplay.grid(column=1,row=0,columnspan=2,pady=10)

#Images - displays don't work yet
# beforeImageLabel = Label(mainframe, text="Before Image", width=35, height=15, relief="solid")
# beforeImageLabel.grid(column=0, row=1, padx=10, pady=10)

# afterImageLabel = Label(mainframe, text="After Image", width=35, height=15, relief="solid")
# afterImageLabel.grid(column=1, row=1, padx=10, pady=10)

# def displayImage(path, labelWidget):
#     '''Loads and displays input and output images in their respective label widgets.'''
#     img = Image.open(path)
#     img = img.resize((300, 300))  #Resizes the image to fit the label
#     img_tk = ImageTk.PhotoImage(img)
#     labelWidget.configure(image=img_tk)
#     labelWidget.image = img_tk  #Keeps a reference to avoid garbage collection

#Buttons
def openCommand():
    '''Generates tkinter file dialog and
    passes selection to the conversion module.
    Module passes back a keyword "OK" on success or provides
    detail if an exception occurs.'''
    path = filedialog.askopenfile(filetypes=[("WEBP files", "*.webp")])
    if path:
        status = interface.fileOpen(path.name) #Updates the filepath display
        if status == "OK":
            pass
            #displayImage(path.name, beforeImageLabel) #Displays the original image
        else:
            messagebox.showinfo(message=status)

def convertCommand():
    '''Calls conversion method and generates
    a save dialog on completion.'''
    interface.fileConvert()
    savePath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if savePath:
        interface.fileSave(savePath)
        #displayImage(savePath, afterImageLabel)  # Display the converted image

buttonFrame = ttk.Frame(mainframe)
buttonFrame.grid(column=0,row=2,columnspan=2,pady=20)

openButton = ttk.Button(buttonFrame, text="Open", command=openCommand)
openButton.grid(column=0, row=0, padx=5)

convertButton = ttk.Button(buttonFrame, text="Convert", command=convertCommand)
convertButton.grid(column=1, row=0, padx=5)

closeButton = ttk.Button(buttonFrame, text="Close", command=root.quit)
closeButton.grid(column=2, row=0, padx=5)


if __name__ == '__main__':
    #
    #Initialize GUI with above config
    #
    root.mainloop()