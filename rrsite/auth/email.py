from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.utils.timezone import now

from rrsite.models import EmailVerifyRecord
from rrsite.util.utils import random_str
from RRWeb.settings import EMAIL_FROM


def send_email(email, send_type='code'):
    try:
        if send_type == 'register':
            code = random_str(16)
            email_title = "RRWeb网站注册"
            email_body = "点击下面链接激活RRWeb账号：http://58.87.109.246/email/verify/{0}?email={1}&type=register".format(code, email)
            result = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if result == 1:
                email_record, created = EmailVerifyRecord.objects.get_or_create(email=email, send_type=send_type)
                email_record.code = str(code)
                email_record.send_time = now
                email_record.save()
                return 1
        elif send_type == 'code':
            email_title = "RRWeb验证码"
            code = random_str(4)
            email_body = "您的验证码为：  {0}".format(code)
            result = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if result == 1:
                email_record, created = EmailVerifyRecord.objects.get_or_create(email=email, send_type=send_type)
                email_record.code = str(code)
                email_record.send_time = now
                email_record.save()
                return 1
        elif send_type == 'change':
            code = random_str(16)
            email_title = "RRWeb邮箱修改验证"
            email_body = "点击下面链接激活RRWeb账号：http://58.87.109.246/email/verify/{0}?email={1}&type=change".format(code, email)
            result = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if result == 1:
                email_record, created = EmailVerifyRecord.objects.get_or_create(email=email, send_type=send_type)
                email_record.code = str(code)
                email_record.send_time = now
                email_record.save()
                return 1
        return 0
    except IntegrityError as e:
        print(e)
        return -1


def check_email_code(email, code, send_type):
    try:
        email_record = EmailVerifyRecord.objects.filter(email__iexact=email, code=code, send_type=send_type)
        if email_record:
            return True
    except Exception as e:
        print(e)
    return False
