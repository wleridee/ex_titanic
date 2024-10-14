from typing import Optional

from pydantic import BaseModel


class TitanicPassengerEntity(BaseModel):
    id: Optional[int]
    has_survived: bool
    passenger_class: int
    name: str
    sex: str
    age: Optional[float]
    siblings_and_spouses_number: int
    parents_and_children_number: int
    ticket_number: str
    fare: float
    cabin_number: Optional[str]
    port_of_embarkation: Optional[str]
