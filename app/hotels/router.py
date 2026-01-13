from datetime import date
from fastapi import APIRouter

from app.exceptions import NotRoomsInLocation
from app.hotels.schemas import SHotels
from app.hotels.service import HotelsService


router = APIRouter(
    prefix="/hotels",
    tags=["Отели & комнаты"]
)

@router.get("")
async def get_hotels() -> list[SHotels]:
    return await HotelsService.find_all()

@router.get("/{location}")
async def get_hotels_in_location(location: str, date_from: date, date_to: date):
    hotels = await HotelsService.find_hotels(location=location, date_from=date_from, date_to=date_to)
    if not hotels:
        raise NotRoomsInLocation
    return hotels

@router.get("/id/{id_hotel}")
async def get_hotel(id_hotel: int) -> SHotels:
    return await HotelsService.find_by_id(id_hotel)