from app.api.dtos.passengers_filters import PassengerFiltersQuery
from app.database.titanic_passenger_repository import TitanicPassengerRepository
from app.domain.titanic_passenger import TitanicPassenger


class TitanicPassengerService:
    def __init__(self, titanic_passenger_repository: TitanicPassengerRepository) -> None:
        self.titanic_passenger_repository = titanic_passenger_repository

    async def create_multiple(self, passengers: list[TitanicPassenger]):
        return await self.titanic_passenger_repository.create_multiple(passengers)

    async def delete_all(self):
        return await self.titanic_passenger_repository.delete_all()

    async def get_all(self, limit: int, offset: int, titanic_passengers_filters: PassengerFiltersQuery):
        return await self.titanic_passenger_repository.get_all(limit, offset, titanic_passengers_filters)

    async def get(self, id: int):
        return await self.titanic_passenger_repository.get(id)
