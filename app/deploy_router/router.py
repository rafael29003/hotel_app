
from fastapi import APIRouter


router = APIRouter(
    prefix="/deploy",
    tags=["Тест для деплоя на vps"],
)

@router.get("")
async def test_router():
    return {"status" : "ok"}


@router.get("/new1")
async def test_router2():
    return {"status" : "ok"}