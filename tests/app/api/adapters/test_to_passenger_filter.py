from pydantic import ValidationError
import pytest
from app.api.adapters.to_passenger_filter import PassengerFiltersQuery, to_passenger_filter


def test_to_passenger_filter_all_params():
    query = PassengerFiltersQuery(
        has_survived=True,
        passenger_class="UPPER",
        name="John",
        sex="MALE",
        age=30.0,
        ticket_number="A123",
        port_of_embarkation="SOUTHAMPTON",
        limit=50,
        offset=10
    )

    expected_filter = {
        'has_survived': True,
        'passenger_class': 1,
        'name': {'contains': 'John'},
        'sex': 'male',
        'age': 30.0,
        'ticket_number': {'contains': 'A123'},

        'port_of_embarkation': 'S',
    }

    result = to_passenger_filter(query)
    assert result == expected_filter


def test_to_passenger_filter_partial_params():
    query = PassengerFiltersQuery(
        has_survived=False,
        passenger_class="LOWER",
        name=None,
        sex="FEMALE",
        age=None,
        ticket_number=None,
        port_of_embarkation=None,
        limit=100,
        offset=0
    )

    expected_filter = {
        'has_survived': False,
        'passenger_class': 3,  # Assuming 'LOWER' is mapped to 3 in PassengerClass enum
        'sex': 'female',  # Assuming 'FEMALE' is mapped to 'F' in Sex enum
    }

    result = to_passenger_filter(query)
    assert result == expected_filter


def test_to_passenger_filter_no_params():
    query = PassengerFiltersQuery()

    expected_filter = {}

    result = to_passenger_filter(query)
    assert result == expected_filter


def test_to_passenger_filter_invalid_passenger_class():
    with pytest.raises(ValidationError):  # Assuming invalid enum raises KeyError
        query = PassengerFiltersQuery(
            passenger_class="INVALID_CLASS"
        )
        to_passenger_filter(query)
