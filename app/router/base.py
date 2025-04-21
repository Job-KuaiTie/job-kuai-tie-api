from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_main():
    return {"msg": "Hello World"}
