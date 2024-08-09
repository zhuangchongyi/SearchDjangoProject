import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json


# 通用返回实体
@dataclass_json
@dataclass
class R:
    code: int
    msg: str
    date: datetime
    data: object

    def __init__(self, code: int = 200, msg: str = 'ok', data: object = None):
        self.code = code
        self.msg = msg
        self.date = datetime.datetime.now()
        self.data = data


# 产品类
@dataclass_json
@dataclass
class Product:
    name: str
    score: float

    def __init__(self, name: str = None, score: float = 0.0):
        self.name = name
        self.score = score
