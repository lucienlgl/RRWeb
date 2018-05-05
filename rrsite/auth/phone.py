from random import randint


def random_phone_code(length=4):
    result = ''
    for i in range(0, length):
        result = result + str(randint(0, 9))
    return result


def send_phone_code(phone, code):
    return True


def check_phone_code(phone, code):
    return True
