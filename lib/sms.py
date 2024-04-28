from threading import Thread
from kavenegar import *
from django.conf import settings


def send_otp_handler(phone_number, password):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': 'otp',
            'token': password,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e.args[0].decode('utf-8'))
    except HTTPException as e:
        print(e.args[0].decode('utf-8'))


def send_tracking_code_handler(phone_number, tracking_code):
    print(f"{phone_number} : {tracking_code}")
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': 'tracking_code',
            'token': tracking_code,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e.args[0].decode('utf-8'))
    except HTTPException as e:
        print(e.args[0].decode('utf-8'))


def send_buy_message_handler(phone_number, buy_number):
    print(f"{phone_number} : {buy_number}")
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': 'buy',
            'token': buy_number,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e.args[0].decode('utf-8'))
    except HTTPException as e:
        print(e.args[0].decode('utf-8'))


def send_otp(phone_number, password):
    thread = Thread(target=send_otp_handler, args=(phone_number, password), daemon=True)
    thread.start()
    thread.join()


def send_tracking_code(phone_number, tracking_code):
    thread = Thread(target=send_tracking_code_handler, args=(phone_number, tracking_code), daemon=True)
    thread.start()
    thread.join()


def send_buy_message(phone_number, buy_number):
    thread = Thread(target=send_tracking_code_handler, args=(phone_number, buy_number), daemon=True)
    thread.start()
    thread.join()
