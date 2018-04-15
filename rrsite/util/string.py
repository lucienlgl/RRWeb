import re
from random import randint

from RRWeb.settings import LOGIN_METHOD


def random_str(length=16):
    str_random = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890_'
    chars_length = len(chars) - 1
    for i in range(length):
        str_random += chars[randint(0, chars_length)]
    return str_random


def username_type(username):
    email_regex = r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$"
    phone_regex = r"1[358][\d]{9}"
    match_obj = re.match(email_regex, username)
    if match_obj:
        return LOGIN_METHOD.get('email', -1)
    match_obj = re.match(phone_regex, username)
    if match_obj:
        return LOGIN_METHOD.get('phone', -1)
    return LOGIN_METHOD.get('no_method', -1)
