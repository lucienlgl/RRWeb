import re
from random import randint

from RRWeb.settings import LOGIN_METHOD, EMAIL_REGEX, PHONE_REGEX


def random_str(length=16):
    str_random = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890_'
    chars_length = len(chars) - 1
    for i in range(length):
        str_random += chars[randint(0, chars_length)]
    return str_random


def username_type(username):
    match_obj = re.match(EMAIL_REGEX, username)
    if match_obj:
        return LOGIN_METHOD.get('email', -1)
    match_obj = re.match(PHONE_REGEX, username)
    if match_obj:
        return LOGIN_METHOD.get('phone', -1)
    return LOGIN_METHOD.get('no_method', -1)


def valid_email(email):
    match_obj = re.match(EMAIL_REGEX, email)
    if match_obj:
        return True
    return False


def valid_phone(phone):
    match_obj = re.match(PHONE_REGEX, phone)
    if match_obj:
        return True
    return False
