from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from pydantic import UUID4, AfterValidator, BaseModel, Field, model_validator
from store.schemas.base import BaseSchemaMixin, OutMixin
from bson import Decimal128


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Nome do produto")
    quantity: int = Field(..., description="Quantidade do produto")
    price: Decimal = Field(..., description="Preço do produto")
    status: bool = Field(..., description="Status do produto")
    
class ProductIn(ProductBase, BaseSchemaMixin):
    ...
    
class ProductOut(ProductIn, OutMixin):
    ...
    
def convert_decimal_128(v):
    return Decimal128(str(v))

Decimal = Annotated[Decimal, AfterValidator(convert_decimal_128)]
class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Quantidade do produto")
    price: Optional[Decimal_] = Field(None, description="Preço do produto")
    status: Optional[bool] = Field(None, description="Status do produto")
    
class ProductUpdateOut(ProductOut):
    ...