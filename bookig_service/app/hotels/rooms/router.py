from datetime import date
from app.hotels.rooms.schemas import SRooms
from app.hotels.rooms.service import RoomsService
from app.hotels.router import router


@router.get("/{hotels_id}/rooms")
async def get_rooms(hotels_id: int, date_from: date, date_to: date):
    return await RoomsService.find_all_rooms(hotels_id, date_from, date_to)