import datetime

import fastapi
from fastapi.routing import APIRouter
from databases import Database
from pydantic import BaseModel, validator
from datetime import date, datetime

food_db = Database("sqlite:///./resources/private/db/datahub.sqlite")


async def db_connect():
    await food_db.connect()


async def db_disconnect():
    await food_db.disconnect()


router = APIRouter(
    prefix="/stash",
    on_startup=[db_connect],
    on_shutdown=[db_disconnect],
    include_in_schema=True,
)


class Food(BaseModel):
    id: int
    count: int
    description: str
    amount: int
    unit: str
    expiry_date: date
    box: int

    @validator('expiry_date', pre=True)
    def _validate_date(cls, value: str) -> date:
        return datetime.strptime(
            value,
            "%m-%d-%Y"
        ).date()


@router.get("/", response_class=fastapi.responses.JSONResponse)
async def show_all():
    query = await food_db.fetch_all("SELECT * FROM FOOD_RESERVES;")
    return [Food(**{key: value for key, value in zip(Food.__fields__, f)}) for f in query]
