# gmail lesssecure app
# https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3ZTd09qX1hyTW9WS21iS0Q0bDVXWkFyclhzd3xBQ3Jtc0ttTlM1bUhjemZ0LWJQcVBKa0d5UEliN19IbzZFWW12S0VaZXVSUkNWVElYS2FRdkhjM20zal9Yblk5bld2QVpSM3dEX0Nka3RVdnBPRXZhalU1bk5ESHNKZUVvR0NhT1hjTjVYbWxoU25wRUpSQTFZZw&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps
# https://myaccount.google.com/u/4/lesssecureapps?rapt=AEjHL4Pa35dKGPcMTwNAUdK7UpYjwKI76nMW3lpr_Hex3NGmT5SwLpaUs4p_mRbmZA1797Pk2-lfdsFkimCj2BtG8ZRk5Uh0qg

# code
import os
from email.contentmanager import maintype, subtype
from email.mime.application import MIMEApplication

import config
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
import smtplib
import mysql.connector
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nayan@123",
    database="attendance"
)

'''
def send_email(subject, msg, file):
    msg = MIMEMultipart()
    # Add body to email
    # open and read the CSV file in binary
    with open(f'AttendanceCSV/{file}.csv', 'r') as f:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(f.read(), Name=file))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_ADDRESS, config.PASSWORD)
    message = 'Subject: {}\n\n{}'.format(subject, msg)
    server.sendmail(config.EMAIL_ADDRESS, 'n.mandliya@somaiya.edu', message)
    server.quit()
    print("Success: Email sent!")
'''

def deleteCSV(fileName):
    cursor = database.cursor()
    cursor.execute("TRUNCATE tempAtt")
    file = f'AttendanceCSV/{fileName}.csv'
    if (os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")


def send_email(subject, msg, file, emailto):
    emailfrom = "n.mandliya@somaiya.edu"
    # emailto = ["n.mandliya@somaiya.edu"]
    fileToSend = f"AttendanceCSV/{file}.csv"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = "YOUR EMAIL SUBJECT"
    msg.preamble = "YOUR EMAIL SUBJECT"

    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_ADDRESS, config.PASSWORD)
    message = 'Subject: {}\n\n{}'.format(subject, msg)
    server.sendmail(emailfrom, emailto, msg.as_string())
    # server.sendmail(config.EMAIL_ADDRESS, 'n.mandliya@somaiya.edu', message)
    server.quit()
    print("Success: Email sent!")
    deleteCSV(file)


subject = "Test subject"
msg = "This is an auto-generated email sent using python"
# send_email(subject, msg, file)

