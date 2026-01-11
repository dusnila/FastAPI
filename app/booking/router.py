from datetime import date
from fastapi import APIRouter, Depends

from app.booking.schemas import SBooking
from app.booking.service import BookingService
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_curret_user
from app.users.models import Users


router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"],
)


@router.get("")
async def get_booking(user: Users = Depends(get_curret_user)) -> list[SBooking]:
    return await BookingService.find_all(user_id=user.id) 


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_curret_user),
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    