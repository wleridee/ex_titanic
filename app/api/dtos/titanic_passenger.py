from pydantic import BaseModel
from typing import Optional


class TitanicPassengerRequest(BaseModel):
    id: int
    survival: int
    pclass: int
    sex: str
    age: Optional[float]
    name: str
    sibsp: int
    parch: int
    ticket: str
    fare: float
    cabin: Optional[str]
    embarked: str


class TitanicPassengerPres(BaseModel):
    id: int
    has_survived: bool
    passenger_class: str
    sex: str
    age: Optional[float]
    name: str
    siblings_and_spouses_number: int
    parents_and_children_number: int
    ticket_number: str
    fare: float
    cabin_number: Optional[str]
    port_of_embarkation: Optional[str]
