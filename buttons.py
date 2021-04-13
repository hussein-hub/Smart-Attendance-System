from tkinter import *

root = Tk()


def click():
    my_label = Label(root, text='button Clicked')
    my_label.grid( column=0)


button = Button(root, text='Click Me', command=click)
# button.pack(side=TOP)
button.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()
