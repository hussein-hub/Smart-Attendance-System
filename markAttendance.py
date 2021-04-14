import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nayan@123",
    database="attendance"

)
temp = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nayan@123",
    database="attendance"
)


def fetchData(name):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    cur = temp.cursor()
    sql = "INSERT INTO tempAtt (fullname, Roll_no, status) VALUES (%s, %s, %s)"

    cur.execute("SELECT * FROM tempAtt")
    markedData = cur.fetchall()
    flag = True
    for i in data:
        fetchedName = i[1] + ' ' + i[2]
        for j in markedData:
            if j[0] == fetchedName:
                flag = False
        if flag:
            if fetchedName == name:
                print(i[3])
                val = (fetchedName, str(i[3]), 'Present')
                cur.execute(sql, val)
    temp.commit()

    database.commit()


def checkDatabase():
    curs = temp.cursor()
    curs.execute("SELECT * FROM tempAtt")
    dataAtt = curs.fetchall()
    print(dataAtt)
    if len(dataAtt) > 0:
        flag = True
        curs1 = database.cursor()
        curs1.execute("SELECT * FROM students")
        fullData = curs1.fetchall()
        for i in fullData:
            flag = True
            for j in dataAtt:
                if i[3] == j[1]:
                    flag = False
            if flag:
                sql = "INSERT INTO tempAtt (fullname, Roll_no, status) VALUES (%s, %s, %s)"
                fetchedName = i[1] + " " + i[2]
                val = (fetchedName, str(i[3]), 'Absent')
                curs1.execute(sql, val)
        database.commit()
        temp.commit()
        return True
    else:
        temp.commit()
        return False