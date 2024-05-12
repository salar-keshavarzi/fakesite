import requests
import json
from django.conf import settings

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش"
callback_url = settings.DOMAIN + 'order/buy/verify/'


def send_request(amount):
    data = {
        "MerchantID": settings.ZP_MERCHANT,
        "Amount": amount,
        "Description": description,
        "CallbackURL": callback_url,
    }
    raw_data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(raw_data))}
    try:
        response = requests.post(url=ZP_API_REQUEST, data=raw_data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            print(response)
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return {'status': False, 'code': 'error'}
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(amount, authority):
    data = {
        "MerchantID": settings.ZP_MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    raw_data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(raw_data))}
    response = requests.post(ZP_API_VERIFY, data=raw_data, headers=headers)
    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'ref_id': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return {'status': False, 'code': 'error'}
