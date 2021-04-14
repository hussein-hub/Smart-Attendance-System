import mysql.connector
import datasetCreation
import preproccess as process
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nayan@123",
    database="attendance"
)


def insert(studentFName, studentLName, roll_no_object, id, fname, lname, roll_no):
    cursor = database.cursor()
    sql = "INSERT INTO students (id, Fname, Lname, Roll_no) VALUES (%s, %s, %s, %s)"
    val = (id, fname, lname, roll_no)
    cursor.execute(sql, val)

    database.commit()
    print(cursor.rowcount, "record inserted.")
    path = datasetCreation.createDirectory(fname, lname)
    datasetCreation.takePhotos(path)
    studentFName.delete(0, 'end')
    studentLName.delete(0, 'end')
    roll_no_object.delete(0, 'end')
    process.preprocessImages()

