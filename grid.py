from tkinter import *


# def createWindow(className, height, width):
#     window = Tk(className=className)
#     window.geometry(f'{height}x{width}')
#     return window


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()

    myLabel = Label(root, text='Hello World')
    myLabel2 = Label(root, text='Hello')
    myLabel.grid(row=1, column=1)
    myLabel2.grid(row=0, column=0)
    # myLabel.pack()

    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
