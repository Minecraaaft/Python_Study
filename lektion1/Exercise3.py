

from tkinter import *
from tkinter import scrolledtext
import math

def isItPrime(number):
    for i in range(2, int(math.sqrt(number) + 1)):
        if (number % i) == 0:
            return False
    return True


window = Tk()
window.geometry("350x400")
frame = Frame(window)
frame.pack(side=TOP)

middleFrame = Frame(window)
middleFrame.pack()

inputFrame = Frame(window)
inputFrame.pack(side=BOTTOM)

window.title("Prime checker")

def change():
    inputNumber = inputEntry.get()

    if isItPrime(int(inputNumber)):
        #txt.insert(0, "This is indeed a prime number")
        txt.delete('1.0', END)
        txt.insert(INSERT, "This is indeed a prime number")
    else:
        #txt.insert(0, "This is not a prime number")
        txt.delete('1.0', END)
        txt.insert(INSERT, "This is not a prime number")


lbl = Label(frame, text="Hej, velkommen til mit program")
lbl.pack()

btnQuit = Button(middleFrame, text="QUIT", fg="red", command=quit)
btnQuit.pack(side=TOP)

btnChange = Button(middleFrame, text="Calculate", command=change)
btnChange.pack()

txt = scrolledtext.ScrolledText(middleFrame, width=40, height=10)
txt.pack(side=BOTTOM)

inputEntry= Entry(inputFrame, width=10)
inputEntry.pack(side=RIGHT, padx=10, pady=10)

lblName = Label(inputFrame, text="Indtast positiv hel tal:")
lblName.pack(side=LEFT)

window.mainloop()