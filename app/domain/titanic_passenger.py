from enum import Enum
from typing import Optional
from pydantic import BaseModel


class PassengerClass(Enum):
    UPPER = 1
    MIDDLE = 2
    LOWER = 3


class Sex(Enum):
    MALE = "male"
    FEMALE = "female"


class EmbarkationPort(Enum):
    CHERBOURG = "C"
    QUEENSTOWN = "Q"
    SOUTHAMPTON = "S"


class TitanicPassenger(BaseModel):
    id: Optional[int]
    has_survived: bool
    passenger_class: PassengerClass
    name: str
    sex: Sex
    age: Optional[float]
    siblings_and_spouses_number: int
    parents_and_children_number: int
    ticket_number: str
    fare: float
    cabin_number: Optional[str]
    port_of_embarkation: Optional[EmbarkationPort]
