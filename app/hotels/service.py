from datetime import date

from sqlalchemy import and_, func, or_, select
from app.booking.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.database import async_session_maker


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def find_hotels(
        cls,
        location: str, 
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            Booking_hotels = (
                select(Rooms)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    and_(
                        Hotels.location.ilike(f"%{location}%"),
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from)
                        )
                    )
                )
                .join(Hotels, Rooms.hotel_id == Hotels.id)
            ).cte("Booking_hotels")

            Hotels_left = (
                select(
                    Hotels.__table__.columns,
                    (Hotels.rooms_quantity - func.count(Booking_hotels.c.hotel_id)).label("rooms_left")
                )
                .select_from(Hotels)
                .join(Booking_hotels, Booking_hotels.c.hotel_id == Hotels.id, isouter=True)
                .where(Hotels.location.ilike(f"%{location}%"))
                .group_by(Hotels.id)
                .having((Hotels.rooms_quantity - func.count(Booking_hotels.c.hotel_id)) > 0)
            )

            result = await session.execute(Hotels_left)
            all_results = result.mappings().all()
            return all_results
