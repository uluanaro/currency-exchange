class Currency():
    def __init__(self, id, name, code, sign):
        self.id = id
        self.name = name
        self.code = code
        self.sign = sign

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'code': self.code,
                'sign': self.sign
                }