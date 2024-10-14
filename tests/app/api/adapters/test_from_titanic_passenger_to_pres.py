import pytest
from app.api.dtos.titanic_passenger import TitanicPassengerPres
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger
from app.api.adapters.from_titanic_passenger_to_pres import from_titanic_passenger_to_pres, from_titanic_passengers_to_pres


@pytest.fixture
def sample_passenger():
    return TitanicPassenger(
        id=1,
        has_survived=True,
        passenger_class=PassengerClass.UPPER,
        name="John Doe",
        sex=Sex.MALE,
        age=22.0,
        siblings_and_spouses_number=0,
        parents_and_children_number=0,
        ticket_number="123",
        fare=100.0,
        cabin_number="C123",
        port_of_embarkation=EmbarkationPort.SOUTHAMPTON
    )


@pytest.fixture
def sample_passengers():
    return [
        TitanicPassenger(
            id=1,
            has_survived=True,
            passenger_class=PassengerClass.UPPER,
            name="John Doe",
            sex=Sex.MALE,
            age=22.0,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="123",
            fare=100.0,
            cabin_number="C123",
            port_of_embarkation=EmbarkationPort.SOUTHAMPTON
        ),
        TitanicPassenger(
            id=2,
            has_survived=False,
            passenger_class=PassengerClass.MIDDLE,
            name="Jane Smith",
            sex=Sex.FEMALE,
            age=30.0,
            siblings_and_spouses_number=1,
            parents_and_children_number=1,
            ticket_number="456",
            fare=200.0,
            cabin_number="C456",
            port_of_embarkation=EmbarkationPort.CHERBOURG
        )
    ]


def test_from_titanic_passenger_to_pres(sample_passenger: TitanicPassenger):
    result = from_titanic_passenger_to_pres(sample_passenger)

    expected = TitanicPassengerPres(
        id=1,
        name="John Doe",
        has_survived=True,
        passenger_class="UPPER",
        sex="MALE",
        age=22.0,
        siblings_and_spouses_number=0,
        parents_and_children_number=0,
        ticket_number="123",
        fare=100.0,
        cabin_number="C123",
        port_of_embarkation="SOUTHAMPTON"
    )

    assert result == expected


def test_from_titanic_passengers_to_pres(sample_passengers: list[TitanicPassenger]):
    result = from_titanic_passengers_to_pres(sample_passengers)

    expected = [
        TitanicPassengerPres(
            id=1,
            name="John Doe",
            has_survived=True,
            passenger_class="UPPER",
            sex="MALE",
            age=22.0,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="123",
            fare=100.0,
            cabin_number="C123",
            port_of_embarkation="SOUTHAMPTON"
        ),
        TitanicPassengerPres(
            id=2,
            name="Jane Smith",
            has_survived=False,
            passenger_class="MIDDLE",
            sex="FEMALE",
            age=30.0,
            siblings_and_spouses_number=1,
            parents_and_children_number=1,
            ticket_number="456",
            fare=200.0,
            cabin_number="C456",
            port_of_embarkation="CHERBOURG"
        )
    ]

    assert result == expected
