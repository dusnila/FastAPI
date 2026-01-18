from datetime import date
from app.database import async_session_maker
from sqlalchemy import and_, delete, func, insert, or_, select

from app.booking.models import Bookings
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.users.models import Users


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add_booking(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            result = await session.execute(get_rooms_left)
            rooms_left: int = result.scalar() or 1

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price_result = await session.execute(get_price) 
                price: int = price_result.scalar() or 0
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def find_all_booking(cls, user_id: int):
        # select *, r.image_id, r.name, r.description, r.services AS image_id, name, description, services
        # from Bookings
        # join rooms r on room_id = r.id
        async with async_session_maker() as session:
            querty = (
                select(
                    *Bookings.__table__.columns,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(querty)
            return result.mappings().all()

    @classmethod
    async def delete(cls, user_id: int, booking_id: int):
        async with async_session_maker() as session:
            querty = (
                delete(Bookings)
                .where(and_(Bookings.id == booking_id, Bookings.user_id == user_id))
                .returning(Bookings)
            )
            result = await session.execute(querty)
            await session.commit()
            return result.mappings().first()
