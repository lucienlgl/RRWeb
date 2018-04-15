from django.core.mail import send_mail

from rrsite.models import *
from rrsite.util.string import random_str
from RRWeb.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
    try:
        email_record = EmailVerifyRecord()
        code = random_str(16)
        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type
        email_record.save()
        email_title = "RRWeb网站注册"
        email_body = "点击下面链接激活RRWeb账号：http://127.0.0.1:8000/email/verify/{0}?email={1}".format(code, email)
        return send_mail(email_title, email_body, EMAIL_FROM, [email])
    except Exception as e:
        print(e)
        return -1
