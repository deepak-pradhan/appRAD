from enum import Enum

'''
class Item(SQLModelEntity, table=True):
    id: int = Field(index=True, default=None, primary_key=True)
    name: str
    age: int
    statuse: Status
'''
class Statuse(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
