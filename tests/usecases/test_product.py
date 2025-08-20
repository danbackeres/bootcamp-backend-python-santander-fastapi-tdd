
from uuid import UUID
from store.usecases.product import product_usecase
from store.schemas.product import ProductOut, ProductUpdateOut
import pytest
from store.core.exceptions import BaseException, NotFoundException

async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)
    assert isinstance(result, ProductOut)
    assert result.name == "IPhone"
    
async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)
    assert isinstance(result, ProductOut)
    assert result.name == "IPhone"
    
async def teste_usecases_get_should_not_found():
    with pytest.raises(NotFoundException) as err:
        result = await product_usecase.get(id=UUID("9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"))
    assert err.value.message == "Product not found"
    
async def test_usecases_query_should_return_success():
    result = await product_usecase.query(limit=1)

    assert isinstance(result[0], ProductOut)
    assert result[0].name == "IPhone"

async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = 7.500
    result = await product_usecase.update(id=product_inserted.id, body=product_up)
    assert isinstance(result, ProductUpdateOut)
    
async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True
    
async def test_usecases_delete_should_not_found():
    with pytest.raises(NotFoundException) as err:
        result = await product_usecase.delete(id=UUID("9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"))
    assert err.value.message == "Product not found"