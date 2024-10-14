from httpx import ASGITransport, AsyncClient
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.domain.titanic_passenger import EmbarkationPort, PassengerClass, Sex, TitanicPassenger
from app.exceptions.not_csv_file_exception import NotCsvFileException
from app.exceptions.not_passenger_csv_exception import NotAPassengerCsvException
from app.exceptions.not_found_exception import NotFoundException
from main import app, get_csv_file_service, get_passenger_service

passenger_service_mock = AsyncMock()


def get_passenger_service_mock():
    return passenger_service_mock


app.dependency_overrides[get_passenger_service] = get_passenger_service_mock

csv_file_service_mock = AsyncMock()


def get_csv_file_service_mock():
    return csv_file_service_mock


app.dependency_overrides[get_csv_file_service] = get_csv_file_service_mock


@pytest.fixture
def setup():
    csv_file_service_mock.reset_mock()
    passenger_service_mock.reset_mock()


@pytest.fixture
def valid_csv_file():
    csv_content = "PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked" \
                  "1,1,1,John Doe,male,22,0,0,123,100,C123,S" \
                  "2,0,2,Jane Doe,female,30,1,1,456,200,C456,C"
    return ("test_passengers.csv", csv_content)


@pytest.fixture
def invalid_csv_file():
    csv_content = "PassengerId,Survived\n1,1\n2,0"
    return ("invalid_passengers.csv", csv_content)


@pytest.fixture
def empty_csv_file():
    return ("empty.csv", "")


@pytest.fixture
def passengers():
    return [
        TitanicPassenger(
            id=1,
            has_survived=True,
            passenger_class=PassengerClass.UPPER,
            name="John Doe",
            sex=Sex.MALE,
            age=30,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="123",
            fare=100,
            cabin_number="C123",
            port_of_embarkation=EmbarkationPort.SOUTHAMPTON
        ),
        TitanicPassenger(
            id=2,
            has_survived=False,
            passenger_class=PassengerClass.MIDDLE,
            name="Jane Doe",
            sex=Sex.FEMALE,
            age=28.0,
            siblings_and_spouses_number=1,
            parents_and_children_number=1,
            ticket_number="456",
            fare=200,
            cabin_number="C456",
            port_of_embarkation=EmbarkationPort.CHERBOURG
        )]


@pytest.fixture
def sample_passenger():
    return (
        TitanicPassenger(
            id=1,
            has_survived=True,
            passenger_class=PassengerClass.UPPER,
            name="John Doe",
            sex=Sex.MALE,
            age=30,
            siblings_and_spouses_number=0,
            parents_and_children_number=0,
            ticket_number="123",
            fare=100,
            cabin_number="C123",
            port_of_embarkation=EmbarkationPort.SOUTHAMPTON
        ),
        {'id': 1, 'has_survived': True, 'passenger_class': 'UPPER', 'sex': 'MALE', 'age': 30.0, 'name': 'John Doe', 'siblings_and_spouses_number': 0,
            'parents_and_children_number': 0, 'ticket_number': '123', 'fare': 100.0, 'cabin_number': 'C123', 'port_of_embarkation': 'SOUTHAMPTON'}
    )


@pytest.mark.asyncio
async def test_upload_valid_csv(valid_csv_file, passengers, setup):
    file_name, content = valid_csv_file
    csv_file_service_mock.parse.return_value = passengers
    passenger_service_mock.create_multiple.return_value = {
        "created": 2, "duplicates": 0}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/passengers/upload", files={"file": (file_name, content)})

    assert response.status_code == 201
    assert response.json() == {"created": 2, "duplicates": 0}
    csv_file_service_mock.validate_file_name.assert_awaited_once_with(
        file_name)
    csv_file_service_mock.validate_content.assert_awaited_once_with(content)
    csv_file_service_mock.parse.assert_awaited_once()
    passenger_service_mock.create_multiple.assert_awaited_once_with(passengers)


@pytest.mark.asyncio
async def test_upload_invalid_csv_headers(invalid_csv_file, setup):
    file_name, content = invalid_csv_file
    csv_file_service_mock.validate_headers.side_effect = NotAPassengerCsvException(
        "The file got incorrect headers, missing header(s): 3")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/passengers/upload", files={"file": (file_name, content)})

    assert response.status_code == 400
    assert response.json()[
        "detail"] == "The file got incorrect headers, missing header(s): 3"
    csv_file_service_mock.validate_file_name.assert_awaited_once_with(
        file_name)
    csv_file_service_mock.validate_content.assert_awaited_once_with(content)


@pytest.mark.asyncio
async def test_upload_empty_csv(empty_csv_file, setup):
    file_name, content = empty_csv_file
    csv_file_service_mock.validate_content.side_effect = NotCsvFileException(
        "This csv file is empty")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/passengers/upload", files={"file": (file_name, content)})

    assert response.status_code == 400
    assert response.json() == {"detail": "This csv file is empty"}
    csv_file_service_mock.validate_file_name.assert_awaited_once_with(
        file_name)
    csv_file_service_mock.validate_content.assert_awaited_once_with(content)


@pytest.mark.asyncio
async def test_get_passengers(passengers):
    passenger_service_mock.get_all.return_value = passengers

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/passengers?limit=10&offset=0")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    passenger_service_mock.get_all.assert_awaited_once_with(10, 0, {})


@pytest.mark.asyncio
async def test_delete_passengers():
    passenger_service_mock.delete_all.return_value = 5

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.delete("/passengers")
    assert response.status_code == 200
    assert "5 passengers were deleted." in response.text
    passenger_service_mock.delete_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_get_passenger(sample_passenger, setup):
    passenger, expected = sample_passenger
    passenger_service_mock.get.return_value = passenger

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/passengers/1")

    assert response.status_code == 200
    assert response.json() == expected
    passenger_service_mock.get.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_passenger_not_found(setup):
    passenger_service_mock.get.side_effect = NotFoundException(
        "No passenger was found with id: 999")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/passengers/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "No passenger was found with id: 999"}
    passenger_service_mock.get.assert_awaited_once_with(999)
