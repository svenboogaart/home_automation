import smtplib
import threading
from datetime import datetime
from email.mime.text import MIMEText

from settings.settings import Settings


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
                        msg['Subject'] = f"Motion detected {self.__settings.location}"
                        msg['From'] = f"Home security <{self.__settings.mail_from}>"
                        msg['To'] = ', '.join(recipients)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                            smtp_server.login(self.__settings.mail_from, self.__settings.mail_password)
                            smtp_server.sendmail(self.__settings.mail_from, recipients, msg.as_string())

                        self.__last_time_send = int(datetime.timestamp(datetime.now()))
                    except smtplib.SMTPException as e:
                        print(f"SMTP error occurred: {e}")
                    except Exception as e:  # Catch any other unexpected exceptions
                        print(f"An unexpected error occurred: {e}")
                else:
                    print(f"Not sending email, only {elapsed_time} seconds elapsed since last email")

        # Create a new thread and start it
        thread = threading.Thread(target=send_email_in_thread)
        thread.start()

    def get_last_date_send(self):
        return self.__last_time_send
