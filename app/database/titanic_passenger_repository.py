from prisma import Prisma

from app.api.dtos.passengers_filters import PassengerFiltersQuery
from app.database.adapters.from_titanic_passengers import from_titanic_passengers
from app.database.adapters.to_titanic_passengers import to_titanic_passenger, to_titanic_passengers
from app.domain.titanic_passenger import TitanicPassenger
from app.exceptions.not_found_exception import NotFoundException


class TitanicPassengerRepository:
    def __init__(self, db: Prisma):
        self.db = db

    async def create_multiple(self, passengers: list[TitanicPassenger]):
        existing_passengers = await self.db.titanicpassenger.find_many(
            where={"id": {"in": [passenger.id
                                 for passenger in passengers]}}
        )
        existing_ids = [passenger.id for passenger in existing_passengers]

        passengers_to_create = [
            passenger for passenger in passengers if passenger.id not in existing_ids
        ]

        parsed_passengers = from_titanic_passengers(
            passengers=passengers_to_create)

        return {
            "created": await self.db.titanicpassenger.create_many(data=[passenger.model_dump() for passenger in parsed_passengers]),
            "duplicates": len(existing_ids)
        }

    async def get_all(self, limit: int, offset: int, titanic_passengers_filters):
        return to_titanic_passengers(await self.db.titanicpassenger.find_many(take=limit, skip=offset, where=titanic_passengers_filters))

    async def delete_all(self):
        return await self.db.titanicpassenger.delete_many()

    async def get(self, id: int):
        passenger = await self.db.titanicpassenger.find_first(where={
            "id": id
        })
        if not passenger:
            raise NotFoundException(f"No passenger was found with id: {id}")
        return to_titanic_passenger(passenger)
