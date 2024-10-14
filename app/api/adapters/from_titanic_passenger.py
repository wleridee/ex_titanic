from app.api.dtos.titanic_passenger import TitanicPassengerPres
from app.domain.titanic_passenger import TitanicPassenger


def from_titanic_passenger_to_pres(passenger: TitanicPassenger) -> TitanicPassengerPres:
    return TitanicPassengerPres(
        id=passenger.id,
        name=passenger.name,
        has_survived=passenger.has_survived,
        passenger_class=passenger.passenger_class.name,
        sex=passenger.sex.name,
        age=passenger.age,
        siblings_and_spouses_number=passenger.siblings_and_spouses_number,
        parents_and_children_number=passenger.parents_and_children_number,
        ticket_number=passenger.ticket_number,
        fare=passenger.fare,
        cabin_number=passenger.cabin_number if passenger.cabin_number != "" else None,
        port_of_embarkation=passenger.port_of_embarkation.name if passenger.port_of_embarkation != None else None
    )


def from_titanic_passengers(passengers: list[TitanicPassenger]) -> list[TitanicPassengerPres]:
    return [from_titanic_passenger_to_pres(passenger) for passenger in passengers]
