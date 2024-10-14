from typing import Literal, Optional
from pydantic import BaseModel, Field


class PassengerFiltersQuery(BaseModel):
    has_survived: Optional[bool] = None
    passenger_class: Optional[Literal["UPPER", "MIDDLE", "LOWER"]] = None
    name: Optional[str] = None
    sex: Optional[Literal["MALE", "FEMALE"]] = None
    age: Optional[float] = None
    ticket_number: Optional[str] = None
    port_of_embarkation: Optional[Literal["CHERBOURG",
                                          "QUEENSTOWN", "SOUTHAMPTON"]] = None
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)


class PassengerFilters(BaseModel):
    has_survived: Optional[bool] = None
    passenger_class: Optional[int] = None
    name: Optional[dict] = None
    sex: Optional[str] = None
    age: Optional[float] = None
    ticket_number: Optional[dict] = None
    port_of_embarkation: Optional[str] = None
