from sqlalchemy.orm import Session
from .. crud import get_rooms
from .. dependencies import get_db
from typing import Union, List, Literal, TYPE_CHECKING



room_list = get_rooms(db=Session(get_db))