from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter.filedialog import *
import webbrowser
import os


def saveFile():
    file = filedialog.asksaveasfilename(initialfile="Untitled-Textify.txt", defaultextension=".txt",
                                        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if file is None:  # if user cancels the save operation
        return
    else:
        try:
            TxtEdWindow.title(os.path.basename(file))
            file = open(file, "w")
            file.write(textHolder.get(1.0, END))
        except Exception:
            TxtEdWindow.title("Untitled-Textify")
            messagebox.showerror(
                title="Error!", message="Unable to save file!")
        finally:
            file.close()


def newFile():
    TxtEdWindow.title("Untitled-Textify")
    textHolder.delete(1.0, END)


def openFile():
    file = askopenfilename(defaultextension=".txt",
                           file=[("All Files", "*.*"),
                                 ("Text Documents", "*.txt")
                                 ]
                           )

    try:
        TxtEdWindow.title(os.path.basename(file))
        textHolder.delete(1.0, END)
        file = open(file, "r")
        textHolder.insert(1.0, file.read())

    except Exception:
        TxtEdWindow.title("Untitled-Textify")
        messagebox.showerror(title="Error!", message="Unable to open file!")

    finally:
        file.close()


def cutText():
    textHolder.event_generate("<<Cut>>")


def copyText():
    textHolder.event_generate("<<Copy>>")


def pastetext():
    textHolder.event_generate("<<Paste>>")


def fontChange():
    global selectedFontFamily
    selectedFontFamily = fontName.get()
    fontWin = Toplevel(TxtEdWindow)
    fontWin.title("Font customization")
    fontWin.resizable(0, 0)
    main_width = TxtEdWindow.winfo_width()
    main_height = TxtEdWindow.winfo_height()
    fontWin_width = 500
    fontWin_height = 430
    x = TxtEdWindow.winfo_x() + (main_width // 2) - (fontWin_width // 2)
    y = TxtEdWindow.winfo_y() + (main_height // 2) - (fontWin_height // 2)
    fontWin.geometry(f"{fontWin_width}x{fontWin_height}+{x}+{y}")

    fontWin.transient(TxtEdWindow)
    fontWin.grab_set()
    fontWin.focus_set()

    fontWinLabel1 = Label(fontWin,
                          text="Font family:",
                          font=("Arial", 12, "bold"),
                          justify=LEFT,
                          width=50,
                          anchor=W
                          )
    fontWinLabel1.grid(row=0, column=0, padx=25, pady=25, sticky=W)

    fontWinLabel2 = Label(fontWin,
                          text="Click the button below to view or change the font from the list.",
                          font=("Arial", 10, "italic"),
                          justify=LEFT,
                          width=50,
                          anchor=W
                          )
    fontWinLabel2.grid(row=1, column=0, padx=25, sticky=W)

    fontChangeVar = StringVar(fontWin)
    fontChangeVar.set(selectedFontFamily)
    txtFont = OptionMenu(fontWin, fontChangeVar, *font.families())
    txtFont.grid(row=2, column=0, padx=150, pady=25, sticky=W)

    def updateFontVar(*args):
        global selectedFontFamily
        selectedFontFamily = fontChangeVar.get()
        fontChangeVar.set(txtFont.cget("text"))
        fontObj = font.Font(family=selectedFontFamily,
                            size=int(fontSize.get()), weight=font.BOLD)
        textHolder.config(font=fontObj)
        fontName.set(selectedFontFamily)
        textHolder.config(font=(fontName.get(), fontSizeSpinbox.get()))

    fontChangeVar.trace("w", updateFontVar)

    fontWinLabel3 = Label(fontWin,
                          text="Current font:",
                          font=("Arial", 10, "bold"),




                          )
    fontWinLabel3.grid(row=2, column=0, padx=25, pady=25, sticky=W)

    fontWinLabel4 = Label(fontWin,
                          text="Font size:",
                          font=("Arial", 12, "bold"),
                          justify=LEFT,
                          width=50,
                          anchor=W
                          )
    fontWinLabel4.grid(row=3, column=0, padx=25, pady=25, sticky=W)

    fontWinLabel5 = Label(fontWin,
                          text="Adjust the font size between 1 and 100.",
                          font=("Arial", 10, "italic"),
                          justify=LEFT,
                          width=50,
                          anchor=W
                          )
    fontWinLabel5.grid(row=4, column=0, padx=25, sticky=W)

    fontSizeSpinbox = Spinbox(fontWin,
                              from_=1,
                              to=100,
                              width=5,
                              textvariable=fontSize,
                              command=updateFontVar
                              )
    fontSizeSpinbox.grid(row=5, column=0, padx=190,
                         pady=25, sticky=W, ipady=2, ipadx=2)
    fontSizeSpinbox.bind("<Key>", lambda e: "break")
    fontSizeSpinbox.config(state="readonly", readonlybackground="white")

    fontWinLabel6 = Label(fontWin,
                          text="Current font size:",
                          font=("Arial", 10, "bold"),
                          justify=LEFT,
                          width=15,
                          anchor=W
                          )
    fontWinLabel6.grid(row=5, column=0, padx=25, pady=25, sticky=W)

    okButton = Button(fontWin,
                      text="OK",
                      width=10,
                      command=fontWin.destroy
                      )
    okButton.grid(row=6, column=0, padx=125, pady=25, sticky=E)

    def restoreFont():
        global selectedFontFamily
        selectedFontFamily = "Consolas"
        fontChangeVar.set(selectedFontFamily)
        fontObj = font.Font(family=selectedFontFamily,
                            size=int(fontSize.get()), weight=font.BOLD)
        textHolder.config(font=fontObj)
        fontName.set(selectedFontFamily)
        fontSize.set("15")
        textHolder.config(font=(fontName.get(), fontSizeSpinbox.get()))

    restoreButton = Button(fontWin,
                           text="Restore default",
                           width=15,
                           command=restoreFont
                           )

    restoreButton.grid(row=6, column=0, padx=25, pady=25, sticky=W)
    fontWin.mainloop()


def textColor():
    global txtColor
    txtColor = colorchooser.askcolor(title="Select a font color")
    textHolder.config(fg=txtColor[1])


txtColor = ["black", "white"]


def Darktheme():
    global txtColor
    if txtColor[1] == "white":
        textHolder.config(bg="black", fg="white", insertbackground="white")
    else:
        textHolder.config(bg="black", fg=txtColor[1], insertbackground="white")
    formatTab.entryconfig("Light Theme".ljust(20), state=NORMAL)
    formatTab.entryconfig("Dark Theme".ljust(21), state=DISABLED)


def Lighttheme():
    global txtColor
    if txtColor[1] == "white":
        textHolder.config(bg="white", fg="black", insertbackground="black")
    else:
        textHolder.config(bg="white", fg=txtColor[1], insertbackground="black")
    formatTab.entryconfig("Light Theme".ljust(20), state=DISABLED)
    formatTab.entryconfig("Dark Theme".ljust(21), state=NORMAL)


def about():
    aboutWin = Toplevel(TxtEdWindow)
    aboutWin.title("About")
    aboutWin.resizable(0, 0)
    aboutWin_width = 500
    aboutWin_height = 400
    x = TxtEdWindow.winfo_x() + (winWidth // 2) - (aboutWin_width // 2)
    y = TxtEdWindow.winfo_y() + (winHeight // 2) - (aboutWin_height // 2)
    aboutWin.geometry(f"{aboutWin_width}x{aboutWin_height}+{x}+{y}")
    aboutWin.transient(TxtEdWindow)
    aboutWin.grab_set()
    aboutWin.focus_set()
    aboutWinLabel1 = Label(aboutWin,
                           text="Textify Version 1.0.1",
                           font=("Arial", 20, "bold"),
                           justify=LEFT,
                           width=50,
                           anchor=W
                           )
    aboutWinLabel1.grid(row=0, column=0, padx=25, pady=25, sticky=W)

    aboutWinLabel2 = Label(aboutWin,
                           text="Textify is a simple text editor developed using Python and Tkinter. It was developed and designed by Anish Dahal on 10/8/2023 for quick text file Read/Write operations in day-to-day life. It is a free and open source software under the MIT License.",
                           wraplength=430,
                           font=("Arial", 11),
                           justify=LEFT,
                           width=100,
                           anchor=W
                           )
    aboutWinLabel2.grid(row=1, column=0, padx=25, sticky=W)

    aboutWinLabel3 = Label(aboutWin,
                           text="© 2023 Textify-Anish Dahal. All Rights Reserved.",
                           font=("Arial", 11,),
                           fg="#3e3f3f",
                           justify=LEFT,
                           width=100,
                           anchor=W
                           )
    aboutWinLabel3.grid(row=2, column=0, padx=25, pady=25, sticky=W)

    aboutWinLabel4 = Label(aboutWin,
                           text="Visit the official website for more information.",
                           font=("Arial", 11,),
                           justify=LEFT,
                           width=100,
                           anchor=W
                           )
    aboutWinLabel4.grid(row=3, column=0, padx=25, pady=25, sticky=W)

    def openWebsite():
        webbrowser.open("https://anishdahal.github.io/Textify/")

    aboutWinLabel5 = Label(aboutWin,
                           text="https://anishdahal.github.io/Textify/",
                           font=("Arial", 11, "underline", "italic"),
                           justify=LEFT,
                           width=30,
                           anchor=W,
                           fg="blue",
                           cursor="hand2"
                           )
    aboutWinLabel5.grid(row=4, column=0, padx=25, sticky=W)
    aboutWinLabel5.bind("<Button-1>", lambda e: openWebsite())

    aboutWinButton = Button(aboutWin,
                            text="OK",
                            width=10,
                            command=aboutWin.destroy
                            )
    aboutWinButton.place(relx=0.94, rely=0.95, anchor=SE)

    aboutWin.mainloop()


def quit():
    TxtEdWindow.destroy()


TxtEdWindow = Tk()
TxtEdWindow.title("Untitled-Textify")
menuTabs = Menu(TxtEdWindow)
TxtEdWindow.config(menu=menuTabs)
file = None

winWidth = 900
winHeight = 500
screenWidth = TxtEdWindow.winfo_screenwidth()
screenHeight = TxtEdWindow.winfo_screenheight()
moveX = int((screenWidth/2)-(winWidth/2))
moveY = int((screenHeight/2)-(winHeight/2))
TxtEdWindow.geometry("{}x{}+{}+{}".format(winWidth, winHeight, moveX, moveY))

fileTab = Menu(menuTabs, tearoff=0)
menuTabs.add_cascade(label="File", menu=fileTab)
fileTab.add_command(label="New File...          Ctrl+N", command=newFile)
fileTab.add_command(label="Open File...        Ctrl+O", command=openFile)
fileTab.add_command(label="Save                    Ctrl+S", command=saveFile)
fileTab.add_separator()
fileTab.add_command(label="Exit", command=quit)

editTab = Menu(menuTabs, tearoff=0)
menuTabs.add_cascade(label="Edit", menu=editTab)
editTab.add_command(label="Cut            Ctrl+X", command=cutText)
editTab.add_command(label="Copy         Ctrl+C", command=copyText)
editTab.add_command(label="Paste         Ctrl+V", command=pastetext)

DarkImg = PhotoImage(file="dark.png")
LightImg = PhotoImage(file="light.png")
DarkImg = DarkImg.subsample(3, 3)
LightImg = LightImg.subsample(2, 2)

formatTab = Menu(menuTabs, tearoff=0)
menuTabs.add_cascade(label="Format", menu=formatTab)
formatTab.add_command(label="Font...", command=fontChange)
formatTab.add_command(label="Color...", command=textColor)
formatTab.add_separator()
formatTab.add_command(label="Light Theme".ljust(
    20), command=Lighttheme, image=LightImg, compound="right", state=DISABLED)
formatTab.add_command(label="Dark Theme".ljust(
    21), command=Darktheme, image=DarkImg, compound="right")

helpTab = Menu(menuTabs, tearoff=0)
menuTabs.add_cascade(label="Help", menu=helpTab)
helpTab.add_command(label="About        Ctrl+Shift+A", command=about)

fontName = StringVar(TxtEdWindow)
fontName.set("Consolas")
fontSize = StringVar(TxtEdWindow)
fontSize.set("15")
textHolder = Text(TxtEdWindow, font=(
    fontName.get(), fontSize.get()), wrap=WORD, undo=True, maxundo=-1)

scrollY = Scrollbar(textHolder)
scrollY.pack(side=RIGHT, fill=Y)
TxtEdWindow.grid_rowconfigure(0, weight=1)
TxtEdWindow.grid_columnconfigure(0, weight=1)
textHolder.grid(sticky=N+E+S+W)
textHolder.config(yscrollcommand=scrollY.set, padx=5, pady=5)

textHolder.focus_set()

textHolder.bind("<Control-Key-O>", lambda e: openFile())
textHolder.bind("<Control-Key-o>", lambda e: openFile())
textHolder.bind("<Control-Key-S>", lambda e: saveFile())
textHolder.bind("<Control-Key-s>", lambda e: saveFile())
textHolder.bind("<Control-Key-N>", lambda e: newFile())
textHolder.bind("<Control-Key-n>", lambda e: newFile())
textHolder.bind("<Control-Key-Q>", lambda e: quit())
textHolder.bind("<Control-Key-q>", lambda e: quit())
textHolder.bind("<Control-Shift-A>", lambda e: about())
textHolder.bind("<Control-Shift-a>", lambda e: about())

TxtEdWindow.mainloop()
