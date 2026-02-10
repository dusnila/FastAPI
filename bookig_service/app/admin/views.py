# from sqladmin import ModelView

# from app.booking.models import Bookings
# from app.hotels.models import Hotels
# from app.hotels.rooms.models import Rooms



# class HotelsAdmin(ModelView, model=Hotels):
#     column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
#     name = "Отель"
#     name_plural = "отели"
#     icon="fa-solid fa-hotel"



# class RoomsAdmin(ModelView, model=Rooms):
#     column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotels, Rooms.booking]
#     name = "Номер"
#     name_plural = "Номера"
#     icon="fa-solid fa-bed"



# class BookingsAdmin(ModelView, model=Bookings):
#     column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]
#     name = "Бронь"
#     name_plural = "Брони"
#     icon="fa-solid fa-book"

