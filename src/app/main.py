from fastapi import FastAPI
from . routers import users, rooms, booking, auth
from . database.init_db import init_database


app = FastAPI()

app.include_router(auth.router, prefix="/token", tags=["Authenticate"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
app.include_router(booking.router, prefix="/booking", tags=["Bookings"])

init_database()
