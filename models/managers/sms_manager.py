from twilio.rest import Client

from settings.settings import Settings


class SmsManager:

    def __init__(self, settings: Settings):
        self.__settings = settings

    def send_sms(self, content):
        if self.__settings.twilio_account_ssd:
            client = Client(self.__settings.twilio_account_ssd, self.__settings.twilio_auth_token)

            message = client.messages.create(
                from_="svenhome",
                body=content,
                to=self.__settings.sms_receiver_number
            )
            self.sms_send_after_alarm_activated = True
            print(f"Sms has been send: {message.sid}")
