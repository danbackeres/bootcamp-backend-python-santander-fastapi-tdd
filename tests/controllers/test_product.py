from typing import List
from tests.factories import product_data
from fastapi import status

async def test_controller_create_should_return_success(client, products_url):
    response = client.post(products_url, json=product_data())
    
    content = response.json()
    del content["id"]
    del content["created_at"]
    del content["updated_at"]
    
    assert response.status_code == status.HTTP_201_CREATED
    
    assert content == {
        "name": "Iphone",
        "quantity": 10,
        "price": "8.500",
        "status": True
    }
    
async def test_controller_get_should_return_success(client, products_url, product_inserted):
    response = await client.get(f"{products_url}{product_inserted.id}")
    
    content = response.json()
    
    del content["created_at"]
    del content["updated_at"]
    
    assert response.status_code == status.HTTP_200_OK
    
    assert content == {
        "id": product_inserted.id,
        "name": "Iphone",
        "quantity": 10,
        "price": "8.500",
        "status": True
    }
    
async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found"}
    
@pytest.mark.usefixtures("product_inserted")
async def test_controller_query_should_return_success(client, products_url, product_inserted):
    response = await client.get(products_url)
    assert response.json() == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1
    
async def test_controller_patch_should_return_success(client, products_url, product_inserted):
    response = await client.patch(f"{products_url}{product_inserted.id}", json={"price": "7.500"})
    
    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": product_inserted.id,
        "name": "Iphone",
        "quantity": 10,
        "price": "7.500",
        "status": True
    }
    
async def test_controller_delete_should_return_no_content(client, products_url, product_inserted):
    response = await client.delete(f"{products_url}{product_inserted.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
async def test_controller_get_delete_return_not_found(client, products_url):
    response = await client.delete(f"{products_url}9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Product not found"}