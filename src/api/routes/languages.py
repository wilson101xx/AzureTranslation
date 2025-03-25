from fastapi import APIRouter
from src.modules.get_language_info import get_language_info

router = APIRouter()

@router.get("/get_languages")
def get_languages():
    """Get a list of available languages."""
    return get_language_info()
