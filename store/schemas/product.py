from typing import Optional
from pydantic import BaseModel, Field
from store.schemas.base import BaseSchemaMixin


class ProductBase(BaseModel):
    name: str = Field(..., description="Nome do produto")
    quantity: int = Field(..., description="Quantidade do produto")
    price: float = Field(..., description="Preço do produto")
    status: bool = Field(..., description="Status do produto")
    
class ProductIn(ProductBase, BaseSchemaMixin):
    ...
    
class ProductOut(ProductIn):
    ...
    
class ProductUpdate(ProductBase):
    quantity: Optional[int] = Field(None, description="Quantidade do produto")
    price: Optional[float] = Field(None, description="Preço do produto")
    status: Optional[bool] = Field(None, description="Status do produto")
    
class ProductUpdateOut(ProductUpdate):
    ...