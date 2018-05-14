
class CustomResponseJson(dict):
    def __init__(self, msg, code, data=None):
        dict.__init__(self, msg=msg, code=code, data=data)
        self.msg = msg
        self.code = code
        self.data = data

    def __repr__(self):
        return dict(code=self.code, msg=self.msg, data=self.data)
