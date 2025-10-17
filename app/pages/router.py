from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/pages", tags=["Страницы"])

templates = Jinja2Templates("app/templates")


@router.get("/hotels")
async def get_hotels_pages(request: Request):
    return templates.TemplateResponse(name="hotels.html", context={"request": request})
