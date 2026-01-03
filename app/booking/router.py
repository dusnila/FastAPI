from fastapi import APIRouter

from app.booking.schemas import SBooking
from app.booking.service import BookingService


router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"],
)


@router.get("")
async def get_booking() -> list[SBooking]:
    return await BookingService.find_all() 