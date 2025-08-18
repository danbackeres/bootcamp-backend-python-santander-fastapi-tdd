from uuid import UUID
from store.schemas.product import ProductIn
import pytest
from pydantic import ValidationError
from test.factories import product_data

def test_schemas_return_sucess():
    data = product_data()
    product = ProductIn.model_validate(data)
    
    assert product.name == "Iphone"
    assert isinstance(product.id, UUID)
    
def test_schemas_return_raise():
    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(name="Iphone", quantity=10, price=8.500)
    
    assert err.value.errors()[0] == {
        'loc': ('status',),
        'msg': 'field required',
        'type': 'value_error.missing'
    }