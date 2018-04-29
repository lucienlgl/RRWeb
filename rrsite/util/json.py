
class CustomResponseJson(object):
    def __init__(self, msg, code, data=[]):
        self.msg = msg
        self.code = code
        self.data = data

    def __str__(self):
        return {'code': self.code, 'msg': self.msg, 'data': self.data}
