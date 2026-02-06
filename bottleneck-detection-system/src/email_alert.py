import smtplib

def send_email(msg):

    sender = "your_email@gmail.com"
    password = "abcdefghijklmnop"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, sender, msg)

    server.quit()
