from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import FileResponse
from databases import Database
from pydantic import BaseModel
from typing import Optional

database = Database("sqlite+aiosqllite:///./resources/private/db/access_codes.db")


class AccessToken(BaseModel):
    token: str
    limit: Optional[int]
    recipient: str


async def db_connect():
    await database.connect()


async def db_disconnect():
    await database.disconnect()


router = APIRouter(
    prefix="/postie", on_startup=[db_connect], on_shutdown=[db_disconnect]
)


@router.get("/fetch/{token}", response_class=FileResponse)
async def fetch(request: Request, token: str):
    # * Check validity of access code
    #   * Access code valid?
    #   * Is code expired time or access count wise?
    # * Get associated resource with the access code
    # * Track access code usage access code
    #   * Increment accesses
    return FileResponse(None, status_code=404)
