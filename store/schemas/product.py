from pydantic import Field
from store.schemas.base import BaseSchemaMixin


class ProductIn(BaseSchemaMixin):
    name: str = Field(..., description="Nome do produto")
    quantity: int = Field(..., description="Quantidade do produto")
    price: float = Field(..., description="Preço do produto")
    status: bool = Field(..., description="Status do produto")