import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_email(to_email, subject, body):
    sender_email = "******"  # 
    sender_password = "*********"  # 

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

   
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, to_email, text)
    server.quit()

