from fastapi import APIRouter

from app.booking.service import BookingService


router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"],
)


@router.get("")
async def get_booking():
    return await BookingService.find_all()