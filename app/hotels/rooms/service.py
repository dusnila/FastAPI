from datetime import date
from sqlalchemy import Integer, and_, cast, func, or_, select
from app.booking.models import Bookings
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.database import async_session_maker


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def find_all_rooms(
        cls, hotels_id: int, date_from: date, date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Rooms)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    and_(
                        Rooms.hotel_id == hotels_id,
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from)
                        )
                    )
                )
            ).cte("Booking_hotels")

            days_count: int = (date_to - date_from).days

            get_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * days_count).label("total_cost"),
                    (Rooms.quantity - func.count(booked_rooms.c.id)).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.id, isouter=True)
                .where(Rooms.hotel_id == hotels_id)
                .group_by(Rooms.id)
            )

        result = await session.execute(get_rooms)
        return result.mappings().all()