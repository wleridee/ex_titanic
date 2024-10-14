import pytest
from app.database.adapters.to_titanic_passengers import to_titanic_passenger, to_titanic_passengers
from app.database.entities import TitanicPassengerEntity
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger

# Sample data for testing


@pytest.fixture
def sample_passenger_entity():
    return TitanicPassengerEntity(
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
def sample_passenger_entities():
    return [
        TitanicPassengerEntity(
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
        ),
        TitanicPassengerEntity(
            id=2,
            has_survived=False,
            passenger_class=2,
            name="Jane Doe",
            sex="female",
            age=28.0,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="A/5 21172",
            fare=7.25,
            cabin_number=None,
            port_of_embarkation="Q"
        )
    ]


def test_to_titanic_passenger(sample_passenger_entity):
    # Act
    result = to_titanic_passenger(sample_passenger_entity)

    # Expected output as a TitanicPassenger object
    expected = TitanicPassenger(
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
    )

    # Assert
    assert result == expected


def test_to_titanic_passengers(sample_passenger_entities):
    # Act
    result = to_titanic_passengers(sample_passenger_entities)

    # Expected output as a list of TitanicPassenger objects
    expected = [
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
            port_of_embarkation=EmbarkationPort.QUEENSTOWN
        )
    ]

    # Assert
    assert result == expected
