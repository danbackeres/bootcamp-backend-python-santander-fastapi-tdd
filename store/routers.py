from fastapi import APIRouter
from store.core.config import settings
from store.controllers.product import router as product

api_router = APIRouter()
api_router.include_router(product, prefix="/products")