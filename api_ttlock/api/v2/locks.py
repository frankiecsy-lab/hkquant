from fastapi import APIRouter
router = APIRouter()

@router.get("/info")
def get_info():
    return {"version": "v2", "status": "enhanced"}