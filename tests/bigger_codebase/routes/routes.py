from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def say_hello() -> dict[str, str]:
    return {"message": "Hello, World!"}
