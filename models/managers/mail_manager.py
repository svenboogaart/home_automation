import threading
from email.mime.text import MIMEText

from settings.settings import Settings
import smtplib
from email.message import EmailMessage
from datetime import datetime

class MailManager:

    def __init__(self, settings: Settings):
        self.__settings = settings
        self.sms_send_after_alarm_activated = False
        self.__last_time_send = 0

    def send_mail(self, message: str, to: str):
        def send_email_in_thread():
            elapsed_time = int(datetime.timestamp(datetime.now())) - self.__last_time_send
            if self.__settings.send_mail:
                if elapsed_time > 60:
                    try:
                        recipients = [to]

                        msg = MIMEText(message)
                        msg['Subject'] = "Motion detected %s" % self.__settings.location
                        msg['From'] = "Home security <%s>" % self.__settings.mail_from
                        msg['To'] = ', '.join(recipients)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                            smtp_server.login(self.__settings.mail_from, self.__settings.mail_password)
                            smtp_server.sendmail(self.__settings.mail_from, recipients, msg.as_string())

                        self.__last_time_send = int(datetime.timestamp(datetime.now()))
                    except Exception as e:
                        print("Failed to send e-mail: %s" % e)
                else:
                    print("Not sending email, only %s seconds elapsed since last email" % elapsed_time)

        # Create a new thread and start it
        thread = threading.Thread(target=send_email_in_thread)
        thread.start()
