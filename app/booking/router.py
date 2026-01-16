from datetime import date
from fastapi import APIRouter, Depends, Response, status

from app.booking.schemas import SBooking, SBookingInfo
from app.booking.service import BookingService
from app.exceptions import BookingNotDeleteExecute, NotBookingsExecute, RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_curret_user
from app.users.models import Users


router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"],
)


@router.get("")
async def get_booking(user: Users = Depends(get_curret_user)):
    bookings = await BookingService.find_all_booking(user.id)
    if not bookings:
        return NotBookingsExecute
    return bookings



@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_curret_user),
) -> SBooking:
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_model = SBooking.model_validate(booking)
    booking_dict = booking_model.model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking
    

@router.delete(
        "/{id_booking}",
        status_code=204,
)
async def delete(
    id_booking: int,
    user: Users = Depends(get_curret_user),
):
    result = await BookingService.delete(user.id, id_booking)
    if not result:
        raise BookingNotDeleteExecute
    return Response(status_code=status.HTTP_204_NO_CONTENT)