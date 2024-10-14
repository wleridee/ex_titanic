from contextlib import asynccontextmanager
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, File, HTTPException, Query, Request, UploadFile

from app.api.adapters.to_passenger_filter import to_passenger_filter
from app.api.adapters.from_titanic_passenger_to_pres import from_titanic_passenger_to_pres, from_titanic_passengers_to_pres
from app.api.dtos.passengers_filters import PassengerFiltersQuery
from app.api.dtos.titanic_passenger import TitanicPassengerPres
from app.database.titanic_passenger_repository import TitanicPassengerRepository
from app.domain.csv_file_service import CsvFileService
import csv
from io import StringIO

from app.exceptions.not_csv_file_exception import NotCsvFileException
from app.exceptions.not_found_exception import NotFoundException
from app.exceptions.not_passenger_csv_exception import NotAPassengerCsvException
from app.database.database import db
from app.domain.titanic_passenger_service import TitanicPassengerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)


def get_passenger_service():
    titanic_passenger_repo = TitanicPassengerRepository(db)
    return TitanicPassengerService(titanic_passenger_repo)


def get_csv_file_service():
    return CsvFileService()


@app.exception_handler(NotCsvFileException)
async def not_csv_file_exception_handler(request: Request, exc: NotCsvFileException):
    raise HTTPException(
        status_code=400, detail=exc.message)


@app.exception_handler(NotAPassengerCsvException)
async def not_a_passenger_csv_exception_handler(request: Request, exc: NotAPassengerCsvException):
    raise HTTPException(
        status_code=400, detail=exc.message)


@app.exception_handler(NotFoundException)
async def not_a_passenger_csv_exception_handler(request: Request, exc: NotFoundException):
    raise HTTPException(
        status_code=404, detail=exc.message)


@app.get("/")
async def get_app():
    return "Application is running."


@app.post("/passengers/upload", status_code=201)
async def upload_csv(
        titanic_passenger_service: Annotated[TitanicPassengerService, Depends(get_passenger_service)],
        csv_file_service: Annotated[CsvFileService, Depends(get_csv_file_service)],
        file: UploadFile = File(...)):
    file_name = file.filename
    await csv_file_service.validate_file_name(file_name)

    content = file.file.read().decode("utf-8").strip()
    await csv_file_service.validate_content(content)

    csv_reader = csv.reader(StringIO(content))
    headers = next(csv_reader)
    await csv_file_service.validate_headers(headers)

    passengers = await csv_file_service.parse(headers, csv_reader)
    return await titanic_passenger_service.create_multiple(passengers)


@app.get("/passengers", response_model=list[TitanicPassengerPres],)
async def get_passengers(
    titanic_passenger_service: Annotated[TitanicPassengerService, Depends(get_passenger_service)],
    filter: Annotated[PassengerFiltersQuery, Query()],
):

    return from_titanic_passengers_to_pres(await titanic_passenger_service.get_all(
        filter.limit,
        filter.offset,
        to_passenger_filter(filter)
    ))


@app.delete("/passengers", response_model=str)
async def delete_passengers(titanic_passenger_service: Annotated[TitanicPassengerService, Depends(get_passenger_service)]):
    return f"{await titanic_passenger_service.delete_all()} passengers were deleted."


@app.get("/passengers/{id}", response_model=TitanicPassengerPres)
async def get_passenger(id: int, titanic_passenger_service: Annotated[TitanicPassengerService, Depends(get_passenger_service)],):
    passenger = await titanic_passenger_service.get(id)
    return from_titanic_passenger_to_pres(passenger)
