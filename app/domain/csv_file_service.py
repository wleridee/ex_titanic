from enum import Enum
from app.exceptions.not_csv_file_exception import NotCsvFileException
from app.exceptions.not_passenger_csv_exception import NotAPassengerCsvException
from app.domain.titanic_passenger import TitanicPassenger

PASSENGER_FILE_HEADERS = ["PassengerId", "Survived", "Pclass", "Name",
                          "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]


class PassengerFileHeaders(Enum):
    PASSENGER_ID = "PassengerId"
    SURVIVED = "Survived"
    PCLASS = "Pclass"
    NAME = "Name"
    SEX = "Sex"
    AGE = "Age"
    SIBSP = "SibSp"
    PARCH = "Parch"
    TICKET = "Ticket"
    FARE = "Fare"
    CABIN = "Cabin"
    EMBARKED = "Embarked"


passenger_file_headers_list = [cls.value for cls in PassengerFileHeaders]
passenger_file_headers = iter(passenger_file_headers_list)


class CsvFileService:
    async def validate_file_name(self, file_name: str):
        if not file_name.endswith(".csv"):
            raise NotCsvFileException("This file has an incorrect extension")

    async def validate_content(self, content: str):
        if content == "":
            raise NotCsvFileException("This csv file is empty")

    async def validate_headers(self, headers):
        missing_headers = list(set(passenger_file_headers_list) - set(headers))
        if len(missing_headers) > 0:
            raise NotAPassengerCsvException(
                f"The file got incorrect headers, missing header(s): {missing_headers}")

    async def parse(self, headers: str, content: str) -> list[TitanicPassenger]:
        header_index = {column: index for index, column in enumerate(headers)}
        data = []

        for row in content:
            id = row[header_index[PassengerFileHeaders.PASSENGER_ID.value]]
            survived = row[header_index[PassengerFileHeaders.SURVIVED.value]]
            pclass = row[header_index[PassengerFileHeaders.PCLASS.value]]
            name = row[header_index[PassengerFileHeaders.NAME.value]]
            sex = row[header_index[PassengerFileHeaders.SEX.value]]
            age = row[header_index[PassengerFileHeaders.AGE.value]]
            sibsp = row[header_index[PassengerFileHeaders.SIBSP.value]]
            parch = row[header_index[PassengerFileHeaders.PARCH.value]]
            ticket = row[header_index[PassengerFileHeaders.TICKET.value]]
            fare = row[header_index[PassengerFileHeaders.FARE.value]]
            cabin = row[header_index[PassengerFileHeaders.CABIN.value]]
            embarked = row[header_index[PassengerFileHeaders.EMBARKED.value]]

            data.append(TitanicPassenger(id=id, has_survived=True if int(survived) == 1 else False,
                        passenger_class=int(pclass), name=name, sex=sex, age=age if age else None, siblings_and_spouses_number=sibsp,
                        parents_and_children_number=parch, ticket_number=ticket, fare=fare, cabin_number=cabin, port_of_embarkation=embarked if embarked else None))

        return data
