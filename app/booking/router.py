from fastapi import APIRouter, Depends

from app.booking.schemas import SBooking
from app.booking.service import BookingService
from app.users.dependencies import get_curret_user
from app.users.models import Users


router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"],
)


@router.get("")
async def get_booking(user: Users = Depends(get_curret_user)):
    return await BookingService.find_all(user_id=user.id) 