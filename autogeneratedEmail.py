# gmail lesssecure app
# https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3ZTd09qX1hyTW9WS21iS0Q0bDVXWkFyclhzd3xBQ3Jtc0ttTlM1bUhjemZ0LWJQcVBKa0d5UEliN19IbzZFWW12S0VaZXVSUkNWVElYS2FRdkhjM20zal9Yblk5bld2QVpSM3dEX0Nka3RVdnBPRXZhalU1bk5ESHNKZUVvR0NhT1hjTjVYbWxoU25wRUpSQTFZZw&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps
# https://myaccount.google.com/u/4/lesssecureapps?rapt=AEjHL4Pa35dKGPcMTwNAUdK7UpYjwKI76nMW3lpr_Hex3NGmT5SwLpaUs4p_mRbmZA1797Pk2-lfdsFkimCj2BtG8ZRk5Uh0qg

# code
import config

import smtplib


def send_email(subject, msg, file):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_ADDRESS, config.PASSWORD)
    message = 'Subject: {}\n\n{}'.format(subject, msg)
    server.sendmail(config.EMAIL_ADDRESS, 'n.mandliya@somaiya.edu', message)
    server.quit()
    print("Success: Email sent!")




subject = "Test subject"
msg = "This is an auto-generated email sent using python"
file = 'AttendanceCSV/1_RDBMS.csv'
send_email(subject, msg, file)

