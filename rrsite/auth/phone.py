from random import randint
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from django.utils.timezone import now

from rrsite.models import PhoneVerifyRecord


def random_phone_code(length=4):
    result = ''
    for i in range(0, length):
        result = result + str(randint(0, 9))
    return result


def send_phone_code(phone, code, minute):
    global result_code
    app_id = 1400082932
    app_key = "4256aeadfa9394ff8728cf40d930e77f"
    params = [str(code), str(minute)]
    template_id = 107886

    s_sender = SmsSingleSender(app_id, app_key)
    err_msg = None
    try:
        result = s_sender.send_with_param(86, phone_number=phone, template_id=template_id, params=params)
        print(result)
        result_code = result.get('result', 0)
        err_msg = result.get('errmsg', '')
        if result_code != 0:
            return result_code, err_msg
        phone_record, created = PhoneVerifyRecord.objects.get_or_create(phone=phone)
        phone_record.code = code
        phone_record.send_time = now
        phone_record.save()
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        return result_code, err_msg


def check_phone_code(phone, code):
    try:
        phone_record = PhoneVerifyRecord.objects.filter(phone=phone)
        if not phone_record:
            return 0, '手机号错误'
        if phone_record[0].code != code:
            return 0, '验证码错误'
        send_time = phone_record[0].send_time
        if (now() - send_time).seconds > 300:
            return 0, '验证码过期'
        return 1, '修改手机号成功'
    except Exception as e:
        print(e)
        return 0, '修改手机号失败'
