from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase import get_async_session
from Converter.models import conversion
from Converter.schemas import ConversionCreate

router = APIRouter(
    prefix="/converter",
    tags=["conversion"]
)

@router.get("/conversion")
def get_conversion_file():
    return "Здесь будет описан метод конвертации файла"