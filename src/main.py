from fastapi import FastAPI
import uvicorn
from . routers import users, rooms, booking, auth

app = FastAPI()

app.include_router(auth.router, prefix="/token", tags=["authentincate"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(booking.router, prefix="/booking", tags=["booking"])

# if __name__ == "__main__":
#   uvicorn.run(app, host="0.0.0.0", port=8000)