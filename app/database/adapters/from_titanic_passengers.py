
from app.database.entities import TitanicPassengerEntity
from app.domain.titanic_passenger import TitanicPassenger


def from_titanic_passenger(passenger: TitanicPassenger) -> TitanicPassengerEntity:
    return TitanicPassengerEntity(
        id=passenger.id,
        name=passenger.name,
        has_survived=passenger.has_survived,
        passenger_class=passenger.passenger_class.value,
        sex=passenger.sex.value,
        age=passenger.age,
        siblings_and_spouses_number=passenger.siblings_and_spouses_number,
        parents_and_children_number=passenger.parents_and_children_number,
        ticket_number=passenger.ticket_number,
        fare=passenger.fare,
        cabin_number=passenger.cabin_number,
        port_of_embarkation=passenger.port_of_embarkation.value if passenger.port_of_embarkation != None else None
    )


def from_titanic_passengers(passengers: list[TitanicPassenger]) -> list[TitanicPassengerEntity]:
    return [from_titanic_passenger(passenger) for passenger in passengers]
