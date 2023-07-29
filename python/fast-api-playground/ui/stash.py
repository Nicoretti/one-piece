import httpx
from pydantic import BaseModel, validator
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from datetime import date, datetime

router = APIRouter(include_in_schema=True)

templates = Jinja2Templates(directory="ui/templates/stash")


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
            "%Y-%m-%d"
        ).date()


@router.get("/foods", response_class=HTMLResponse)
async def foods(request: Request):
    url = 'http://127.0.0.1:8000/api/stash/'
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
        foods = [Food(**{key: value for key, value in zip(Food.__fields__, f.values())}) for f in response.json()]
        return templates.TemplateResponse('food-reserves.html', {'request': request, 'foods': foods})
