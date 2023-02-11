import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send(email, name, code, expired):
    try:
        sender_email = settings.SMTP_USERNAME
        receiver_email = email
        password_email = settings.SMTP_PASSWORD

        message = MIMEMultipart("alternative")
        message["Subject"] = "Kode Aktivasi Pembuatan Akun Tools"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML message
        html = f"""\
            Halo {name}
            <br><br>
            Berikut adalah kode aktivasi pembuatan akun Tools:
            <br><br>
            <table cellspacing='0' cellpadding='0'><tbody><tr><td>Kode aktivasi</td><td>&nbsp;:&nbsp;</td><td><b>{code}</b></td></tr><tr><td>Expired</td><td>&nbsp;:&nbsp;</td><td>{expired}</td></tr></tbody></table>
            <br>
            Silahkan gunakan kode aktivasi sebelum masa berlaku habis (expired).
            <br><br>
            Terima kasih,
            <br>
            Admin Tools
            """

        # Turn these into plain/html MIMEText objects
        content = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(content)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
            server.login(sender_email, password_email)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
            server.quit()
    except smtplib.SMTPResponseException as e:
        print(e.smtp_error)
        print("Sending to: " + receiver_email + " failed!")