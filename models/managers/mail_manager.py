from email.mime.text import MIMEText

from settings.settings import Settings
import smtplib
from email.message import EmailMessage

class MailManager:

    def __init__(self, settings: Settings):
        self.__settings = settings
        self.sms_send_after_alarm_activated = False

    def send_mail(self, message: str, to: str):
        if self.__settings.send_mail:
            try:
                recipients = [to]

                msg = MIMEText(message)
                msg['Subject'] = "Motion detected %s" % self.__settings.location
                msg['From'] =  "Home security <%s>" % self.__settings.mail_from
                msg['To'] = ', '.join(recipients)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(self.__settings.mail_from, self.__settings.mail_password)
                    smtp_server.sendmail( self.__settings.mail_from, recipients, msg.as_string())
            except Exception as e:
                print("Failed to send e-mail: %s" % e)

            # client = Client(self.__settings.twilio_account_ssd, self.__settings.twilio_auth_token)
            #
            # message = client.messages.create(
            #     from_="svenhome",
            #     body=content,
            #     to=self.__settings.sms_receiver_number
            # )
            # self.sms_send_after_alarm_activated = True
            # print(f"Sms has been send: {message.sid}")
            print("TODO implement sending e-mail")
