from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def index():
    return "<html><head></head><body>Hello World!</body></html>"


@router.get("/", response_class=HTMLResponse)
async def index():
    return "<html><head></head><body>Hello World!</body></html>"
