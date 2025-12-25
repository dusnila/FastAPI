from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

app = FastAPI()

class SHotels(BaseModel):
    addres: str
    name: str
    stars: int

class HotelsSearshArgs:
    def __init__(
            self, 
            hotel_id: int,
            location: str,
            date_from: date,
            date_to: date,
            stars: Optional[int] = Query(None, ge=1, le=5),
            has_spa: Optional[bool] = None,
        ):
            self.hotel_id = hotel_id
            self.location = location
            self.date_from = date_from
            self.date_to = date_to
            self.stars = stars
            self.has_spa = has_spa


@app.get("/hotels/{hotel_id}")
def get_hotel(
    search_args: HotelsSearshArgs = Depends()
) -> list[SHotels]:
    

    hotels = [
        {
            "addres": "гигало 18",
            "name": "super hotel",
            "stars": 5,
        },
    ]


    return hotels 


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/booking")
def post_doking(book: SBooking):
    pass
