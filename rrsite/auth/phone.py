from random import randint

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


def random_phone_code(length=4):
    result = ''
    for i in range(0, length):
        result = result + str(randint(0, 9))
    return result


def send_phone_code(phone, code, minute):
    app_id = 1400082932
    app_key = "4256aeadfa9394ff8728cf40d930e77f"
    params = [str(code), str(minute)]
    template_id = 107886

    s_sender = SmsSingleSender(app_id, app_key)
    result = -1
    err_msg = None
    try:
        result = s_sender.send_with_param(86, phone_number=phone, template_id=template_id, params=params)
        result = result.get('result', 0)
        err_msg = result.get('errmsg', '')
        if result != 0:
            print(err_msg)
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    return result, err_msg


def check_phone_code(phone, code):
    return True
