import pytest
from unittest.mock import AsyncMock
from app.database.entities import TitanicPassengerEntity
from app.database.titanic_passenger_repository import TitanicPassengerRepository
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def titanic_passenger_repository(mock_db):
    return TitanicPassengerRepository(mock_db)


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
        ticket_number="123",
        fare=100.0,
        cabin_number="C123",
        port_of_embarkation="S"
    )


@pytest.mark.asyncio
async def test_create_multiple(titanic_passenger_repository, sample_passenger, sample_passenger_entity):
    mock_passengers = [sample_passenger]

    titanic_passenger_repository.db.titanicpassenger.create_many.return_value = 1

    result = await titanic_passenger_repository.create_multiple(mock_passengers)

    assert result == {"created": 1, "duplicates": 0}
    titanic_passenger_repository.db.titanicpassenger.create_many.assert_awaited_once_with(
        data=[sample_passenger_entity.model_dump()])


@pytest.mark.asyncio
async def test_delete_all(titanic_passenger_repository):
    titanic_passenger_repository.db.titanicpassenger.delete_many.return_value = 5

    result = await titanic_passenger_repository.delete_all()

    assert result == 5
    titanic_passenger_repository.db.titanicpassenger.delete_many.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all(titanic_passenger_repository, sample_passenger, sample_passenger_entity):
    titanic_passenger_repository.db.titanicpassenger.find_many.return_value = [
        sample_passenger_entity]

    result = await titanic_passenger_repository.get_all(limit=100, offset=0, titanic_passengers_filters={"filter": "filter"})

    assert result == [sample_passenger]
    titanic_passenger_repository.db.titanicpassenger.find_many.assert_awaited_once_with(
        take=100, skip=0, where={"filter": "filter"})


@pytest.mark.asyncio
async def test_get(titanic_passenger_repository, sample_passenger, sample_passenger_entity):
    titanic_passenger_repository.db.titanicpassenger.find_first.return_value = sample_passenger_entity

    result = await titanic_passenger_repository.get(id=1)

    assert result == sample_passenger
    titanic_passenger_repository.db.titanicpassenger.find_first.assert_awaited_once_with(where={
        "id": 1
    })
