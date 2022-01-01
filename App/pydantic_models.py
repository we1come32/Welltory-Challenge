from datetime import date
from typing import List

from pydantic import BaseModel


class Value(BaseModel):
    date: date
    value: float


class MassValue(BaseModel):
    x_data_type: str
    y_data_type: str
    x: List[Value]
    y: List[Value]


class Data(BaseModel):
    user_id: int
    data: MassValue

