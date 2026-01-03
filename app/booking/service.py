from app.database import async_session_maker
from sqlalchemy import select

from app.booking.models import Bookings
from app.service.base import BaseService

class BookingService(BaseService):
    model = Bookings