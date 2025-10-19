
from fastapi import APIRouter


router = APIRouter(
    prefix="/deploy",
    tags=["Тест для деплоя на vps"],
)

@router.get("")
async def test_router():
    return {"status" : "ok"}