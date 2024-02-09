import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_email(to_email, subject, body):
    sender_email = "leozaitcevic5431@gmail.com"  # Замените на ваш адрес Gmail
    sender_password = "a3S-9X>S86/Z8"  # Замените на ваш пароль Gmail

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # Используйте SMTP сервер Gmail и порт 587 (или 465 для SSL)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Включение шифрования TLS
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, to_email, text)
    server.quit()

