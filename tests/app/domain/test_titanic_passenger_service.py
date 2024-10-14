import pytest
from unittest.mock import AsyncMock
from app.domain.titanic_passenger_service import TitanicPassengerService
from app.database.titanic_passenger_repository import TitanicPassengerRepository
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def titanic_passenger_service(mock_repository):
    return TitanicPassengerService(titanic_passenger_repository=mock_repository)


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


@pytest.mark.asyncio
async def test_create_multiple(titanic_passenger_service, mock_repository, sample_passenger):
    mock_passengers = [sample_passenger]

    mock_repository.create_multiple.return_value = mock_passengers

    result = await titanic_passenger_service.create_multiple(mock_passengers)

    assert result == mock_passengers
    mock_repository.create_multiple.assert_awaited_once_with(mock_passengers)


@pytest.mark.asyncio
async def test_delete_all(titanic_passenger_service, mock_repository):
    mock_repository.delete_all.return_value = 5

    result = await titanic_passenger_service.delete_all()

    assert result == 5
    mock_repository.delete_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all(titanic_passenger_service, mock_repository, sample_passenger):
    mock_passengers = [sample_passenger]
    mock_repository.get_all.return_value = mock_passengers

    result = await titanic_passenger_service.get_all(limit=100, offset=0, titanic_passengers_filters={"filter": "filter"})

    assert result == mock_passengers
    mock_repository.get_all.assert_awaited_once_with(
        100, 0, {"filter": "filter"})


@pytest.mark.asyncio
async def test_get(titanic_passenger_service, mock_repository, sample_passenger):
    mock_repository.get.return_value = sample_passenger

    result = await titanic_passenger_service.get(id=1)

    assert result == sample_passenger
    mock_repository.get.assert_awaited_once_with(1)
