from fastapi import FastAPI
# import uvicorn
from . routers import users, rooms, booking, auth
from . database.init_db import init_database


app = FastAPI()

app.include_router(auth.router, prefix="/token", tags=["authentincate"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(booking.router, prefix="/booking", tags=["booking"])

init_database()
# if __name__ == "__main__":
#   uvicorn.run(app, host="127.0.0.1", port=8000)