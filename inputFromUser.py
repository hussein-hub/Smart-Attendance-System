import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import connect
import random
import csv
import pandas as pd
import recognize
import markAttendance
import pymysql.cursors
import autogeneratedEmail
LARGEFONT = ("Verdana", 35)
teachers = {
    'hussein': ['1234', 'benzenephenol369@gmail.com'],
    'nayan': ['4321', 'n.mandliya@somaiya.edu'],
    'sneha': ['0000', 'sneha.kothi@somaiya.edu'],
}
currentLecture = ['', '']
currentTeacher = ['', '']

def checkCSV(self,controller,dict1, yearInput, subjectInput):
     flag = True
     print(dict1)
     fileName = dict1[0] + '_' + dict1[1]
     print(fileName)
     if not markAttendance.checkDatabase():
         tk.messagebox.showwarning('No Students', 'All students are absent')
     else:
         dbcon = pymysql.connect(host="localhost", user="root", password="Hussein7860@", database="attendance")
         try:
             SQL_Query = pd.read_sql_query(
                 "select * from tempAtt", dbcon)
             df = pd.DataFrame(SQL_Query)
             print(df)
             dbcon.close()

             # deleting CSV
             file = f'AttendanceCSV/{fileName}.csv'
             if (os.path.exists(file) and os.path.isfile(file)):
                 os.remove(file)
                 print("file deleted")
             else:
                 print("file not found")

             # creating new CSV
             df.to_csv(file)
             yearInput.delete(0, 'end')
             subjectInput.delete(0, 'end')
             autogeneratedEmail.send_email('Attendance', f'For {fileName[0]} year, subject {fileName[2:]}', fileName, currentTeacher[1])
         except:
             print("Error")
         print("Mail CSV")

# Teacher Login Page
def verifyTeacher(controller, userName, password):
    print(userName.get())
    print(password.get())
    user = False

    for teacher in teachers.keys():
        if teacher == userName.get():
            if teachers[userName.get()][0] == password.get():
                currentTeacher[0] = userName.get()
                currentTeacher[1] = teachers[userName.get()][1]
                print("Correct")
                userName.delete(0, 'end')
                password.delete(0, 'end')
                return controller.show_frame(selectSubject)
            else:
                print("wrong password")
                user = True
                userName.delete(0, 'end')
                password.delete(0, 'end')
                tk.messagebox.showwarning('Incorrect Password', 'Wrong Password please try again')
                break
    if not user:
        print('wrong username')
        userName.delete(0, 'end')
        password.delete(0, 'end')
        tk.messagebox.showwarning('Incorrect username', 'Wrong username please try again')
        # third window frame registerPage


def showCreateMessage(controller, yearInput, subjectInput):
    tk.messagebox.showwarning('Class Created', 'Attendance will be marked in csv')
    currentLecture[0] = yearInput.get()
    currentLecture[1] = subjectInput.get()
    print(currentLecture)
    df = pd.DataFrame(list())
    df.to_csv(f'AttendanceCSV/{currentLecture[0]}_{currentLecture[1]}.csv')
    return currentLecture, controller.show_frame(StartPage)


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        self.geometry('1000x750')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, loginPage, registerPage, selectSubject):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, loginPage, registerPage respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#accdf5')

        # label of frame Layout 2
        label = tk.Label(self, text="SMART ATTENDANCE SYSTEM", font=LARGEFONT, bg='#accdf5')

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=2, padx=35, pady=10)

        login = tk.Button(self, text='Login', command=lambda: controller.show_frame(loginPage), bg='#accdf5')
        register = tk.Button(self, text='Register', command=lambda: controller.show_frame(registerPage), bg='#accdf5')
        markAttendance = tk.Button(self, text='Mark Attendance', command=lambda: recognize.recognizeStudent(),
                                   bg='#accdf5')

        login.grid(row=1, column=1, padx=10, pady=10)
        register.grid(row=2, column=1, padx=10, pady=10)
        markAttendance.grid(row=3, column=1, padx=10, pady=10)

class selectSubject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#accdf5')

        # label of frame Layout 2
        label = tk.Label(self, text="Select Subject", font=LARGEFONT, bg='#accdf5')

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        year = tk.Label(self, text="Year")
        year.grid(row=2, column=1, pady=10)
        yearInput = tk.Entry(self, width=12, borderwidth=6)
        yearInput.grid(row=2, column=2, pady=10, padx=10)

        subject = tk.Label(self, text="Subject")
        subject.grid(row=3, column=1, pady=10)
        subjectInput = tk.Entry(self, width=12, borderwidth=6)
        subjectInput.grid(row=3, column=2, pady=10, padx=10)

        back = tk.Button(self, text='back', command=lambda: controller.show_frame(StartPage),bg='#accdf5')
        back.grid(row=4, column=2, pady=10)

        create = tk.Button(self, text='Create', command=lambda: showCreateMessage(controller, yearInput, subjectInput), bg='#accdf5')
        create.grid(row=4, column=4, pady=10)

        create = tk.Button(self,text='Send Attendance', command=lambda: checkCSV(self,controller,currentLecture, yearInput, subjectInput), bg='#accdf5')
        create.grid(row=5, column=1, pady=10)

class loginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="LOGIN PAGE", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        tname = tk.Label(self, text="Name")
        tname.grid(row=1, column=1, pady=10)

        userName = tk.Entry(self, width=12, borderwidth=6)
        userName.grid(row=1, column=2, padx=10, pady=10)

        pas = tk.Label(self, text="Password")
        pas.grid(row=2, column=1, pady=10)

        password = tk.Entry(self, width=12, borderwidth=6)
        password.grid(row=2, column=2, padx=10, pady=10)

        back = ttk.Button(self, text="Back",
                          command=lambda: controller.show_frame(StartPage))

        back.grid(row=3, column=1, padx=10, pady=50)

        submit = ttk.Button(self, text="submit",
                            command=lambda: verifyTeacher(controller, userName, password))

        submit.grid(row=3, column=3, padx=10, pady=50)

class registerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Student Registration", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        back = ttk.Button(self, text="Back",
                          command=lambda: controller.show_frame(StartPage))
        back.grid(row=1, column=1, padx=10, pady=10)

        fName = tk.Label(self, text="First Name")
        fName.grid(row=2, column=1, pady=10)
        studentFName = tk.Entry(self, width=12, borderwidth=6)
        studentFName.grid(row=2, column=2, padx=10, pady=10)

        lName = tk.Label(self, text="Last Name")
        lName.grid(row=3, column=1, pady=10)
        studentLName = tk.Entry(self, width=12, borderwidth=6)
        studentLName.grid(row=3, column=2, padx=10, pady=10)

        roll = tk.Label(self, text="Roll Number")
        roll.grid(row=4, column=1, pady=10)
        roll_no = tk.Entry(self, width=12, borderwidth=6)
        roll_no.grid(row=4, column=2, padx=10, pady=10)

        submit = ttk.Button(self, text="submit",
                            command=lambda: connect.insert(studentFName, studentLName, roll_no, random.randint(0,100), studentFName.get(), studentLName.get(), roll_no.get()))

        submit.grid(row=5, column=1, padx=10, pady=10)



app = tkinterApp()
app.mainloop()
