from app.database.entities import TitanicPassengerEntity
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger


def to_titanic_passenger(passenger: TitanicPassengerEntity) -> TitanicPassenger:
    return TitanicPassenger(
        id=passenger.id,
        has_survived=passenger.has_survived,
        passenger_class=PassengerClass(passenger.passenger_class),
        name=passenger.name,
        sex=Sex(passenger.sex),
        age=passenger.age,
        siblings_and_spouses_number=passenger.siblings_and_spouses_number,
        parents_and_children_number=passenger.parents_and_children_number,
        ticket_number=passenger.ticket_number,
        fare=passenger.fare,
        cabin_number=passenger.cabin_number,
        port_of_embarkation=EmbarkationPort(
            passenger.port_of_embarkation) if passenger.port_of_embarkation != None else None
    )


def to_titanic_passengers(passengers: list[TitanicPassengerEntity]) -> list[TitanicPassenger]:
    return [to_titanic_passenger(passenger) for passenger in passengers]
