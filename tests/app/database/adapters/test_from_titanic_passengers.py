import pytest
from app.database.adapters.from_titanic_passengers import from_titanic_passenger, from_titanic_passengers
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger
from app.database.entities import TitanicPassengerEntity


@pytest.fixture
def sample_passenger():
    return TitanicPassenger(
        id=1,
        has_survived=True,
        passenger_class=1,
        name="John Doe",
        sex="male",
        age=22.0,
        siblings_and_spouses_number=0,
        parents_and_children_number=0,
        ticket_number="A/5 21171",
        fare=7.25,
        cabin_number=None,
        port_of_embarkation="C"
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
            ticket_number="A/5 21171",
            fare=7.25,
            cabin_number=None,
            port_of_embarkation=EmbarkationPort.CHERBOURG
        ),
        TitanicPassenger(
            id=2,
            has_survived=False,
            passenger_class=PassengerClass.MIDDLE,
            name="Jane Doe",
            sex=Sex.FEMALE,
            age=28.0,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="A/5 21172",
            fare=7.25,
            cabin_number=None,
            port_of_embarkation=None
        )
    ]


def test_from_titanic_passenger(sample_passenger: TitanicPassenger):
    result = from_titanic_passenger(sample_passenger)

    expected = TitanicPassengerEntity(
        id=1,
        name="John Doe",
        has_survived=True,
        passenger_class=1,
        sex="male",
        age=22.0,
        siblings_and_spouses_number=0,
        parents_and_children_number=0,
        ticket_number="A/5 21171",
        fare=7.25,
        cabin_number=None,
        port_of_embarkation="C"
    )

    assert result == expected


def test_from_titanic_passengers(sample_passengers: list[TitanicPassenger]):
    result = from_titanic_passengers(sample_passengers)

    expected = [
        TitanicPassengerEntity(
            id=1,
            name="John Doe",
            has_survived=True,
            passenger_class=1,
            sex="male",
            age=22.0,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="A/5 21171",
            fare=7.25,
            cabin_number=None,
            port_of_embarkation="C"
        ),
        TitanicPassengerEntity(
            id=2,
            name="Jane Doe",
            has_survived=False,
            passenger_class=2,
            sex="female",
            age=28.0,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="A/5 21172",
            fare=7.25,
            cabin_number=None,
            port_of_embarkation=None
        )
    ]

    assert result == expected
