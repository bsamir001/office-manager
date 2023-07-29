import random
from twilio.rest import Client
from kavenegar import *

'''class SendVerificationCode:
    @staticmethod
    def send(phone_number):
        account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
        auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
        twilio_number = 'YOUR_TWILIO_PHONE_NUMBER'

        code = str(random.randint(1000, 9999))
        message = f'Your verification code is: {code}'

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )

        print(f'Sending verification code {code} to {phone_number}')

class VerifyCode:
    @staticmethod
    def verify(input_code, saved_code):
        return input_code == saved_code'''
from kavenegar import *
#ارسال اسمسم
#ارسال اسمسم

def send_otp_code(phone_number, code):
    try:
        api=KavenegarAPI('4959657358514B4A464342565446584E597170354B414C68724A4D3930507A76492B6E30707865447435343D')
        params={
            'sender':'',
            'receptor':phone_number,
            'message':f'کد تایید شما {code}',
        }
        respance=api.sms_send(params)
        print(respance)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
