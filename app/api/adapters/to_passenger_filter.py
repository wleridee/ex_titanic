from app.api.dtos.passengers_filters import PassengerFilters, PassengerFiltersQuery
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex


def to_passenger_filter(input: PassengerFiltersQuery):
    return PassengerFilters(
        has_survived=input.has_survived,
        passenger_class=PassengerClass[input.passenger_class].value if input.passenger_class else None,
        name={
            "contains": input.name
        } if input.name else None,
        sex=Sex[input.sex].value if input.sex else None,
        age=input.age,
        ticket_number={
            "contains": input.ticket_number
        } if input.ticket_number else None,
        port_of_embarkation=EmbarkationPort[input.port_of_embarkation].value if input.port_of_embarkation else None
    ).model_dump(exclude_none=True)
