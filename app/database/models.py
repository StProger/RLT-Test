from pydantic import BaseModel

from pandas._libs.tslibs.timestamps import Timestamp


class SalaryModel(BaseModel):

    value: int
    dt: Timestamp

    class Config:

        arbitrary_types_allowed = True
