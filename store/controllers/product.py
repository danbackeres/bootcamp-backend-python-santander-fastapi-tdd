from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUseCase

router = APIRouter(tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(body: ProductIn = Body(...), usecase: ProductUseCase = Depends()) -> ProductOut:
    return usecase.create(body=body)

@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)
    
@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(limit: int = 10, usecase: ProductUseCase = Depends()) -> list[ProductOut]:
    return await usecase.query(limit=limit)

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(id: UUID4 = Path(alias="id"), body: ProductUpdate = Body(...), usecase: ProductUseCase = Depends()) -> ProductOut:
    return await usecase.update(id=id, body=body)

@router.delete(path="/{id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete(id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()):
    try:
        await usecase.delete(id=id)
    except NotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)