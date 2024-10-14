import pytest
from app.domain.csv_file_service import CsvFileService
from app.exceptions.not_csv_file_exception import NotCsvFileException
from app.exceptions.not_passenger_csv_exception import NotAPassengerCsvException
from app.domain.titanic_passenger import TitanicPassenger


@pytest.fixture
def csv_service():
    return CsvFileService()


@pytest.mark.asyncio
async def test_validate_file_name_valid(csv_service: CsvFileService):
    # Should not raise an exception
    await csv_service.validate_file_name("passengers.csv")


@ pytest.mark.asyncio
async def test_validate_file_name_invalid(csv_service: CsvFileService):
    with pytest.raises(NotCsvFileException) as exc_info:
        await csv_service.validate_file_name("passengers.txt")
    assert str(exc_info.value) == "This file has an incorrect extension"


@ pytest.mark.asyncio
async def test_validate_headers_valid(csv_service: CsvFileService):
    headers = ["PassengerId", "Survived", "Pclass", "Name", "Sex",
               "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
    # Should not raise an exception
    await csv_service.validate_headers(headers)


@ pytest.mark.asyncio
async def test_validate_headers_missing_header(csv_service: CsvFileService):
    headers = ["PassengerId", "Survived", "Pclass"]  # Missing several headers
    with pytest.raises(NotAPassengerCsvException) as exc_info:
        await csv_service.validate_headers(headers)
    assert "missing header(s)" in str(exc_info.value)


@ pytest.mark.asyncio
async def test_parse_valid(csv_service: CsvFileService):
    headers = ["PassengerId", "Survived", "Pclass", "Name", "Sex",
               "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
    content = [
        ["1", "1", "1", "John Doe", "male", "22",
            "1", "0", "A/5 21171", "7.25", "", "C"],
        ["2", "0", "1", "Jane Doe", "female", "28",
            "1", "0", "PC 17599", "71.2833", "C85", "C"]
    ]

    result = await csv_service.parse(headers, content)

    assert len(result) == 2
    assert result[0] == TitanicPassenger(
        id=1,
        has_survived=True,
        passenger_class=1,
        name="John Doe",
        sex="male",
        age=22,
        siblings_and_spouses_number=1,
        parents_and_children_number=0,
        ticket_number="A/5 21171",
        fare=7.25,
        cabin_number="",
        port_of_embarkation="C"
    )
    assert result[1] == TitanicPassenger(
        id=2,
        has_survived=False,
        passenger_class=1,
        name="Jane Doe",
        sex="female",
        age=28,
        siblings_and_spouses_number=1,
        parents_and_children_number=0,
        ticket_number="PC 17599",
        fare=71.2833,
        cabin_number="C85",
        port_of_embarkation="C"
    )
