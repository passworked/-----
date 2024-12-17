from pydantic import BaseModel
from typing import Literal


class GetAllTable(BaseModel):
    pass

class GetTableByMajor(BaseModel):
    # 字段验证仅允许特定字符串
    major: Literal['测绘', '遥感']

