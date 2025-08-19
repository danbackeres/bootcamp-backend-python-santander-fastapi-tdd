import asyncio
from uuid import UUID
import pytest
from store.db.mongo import db_client
from store.schemas.product import ProductIn,  ProductUpdate
from tests.factories import product_data


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()   

@pytest.fixture
def mongo_client():
    return db_client.get()

@pytest.fixture
async def clear_collection(autouse=True):
    yield
    collections_name = await mongo_client.get_database().list_collection_names()
    for collection in collections_name:
       if collection.startswith("system"): 
           continue
       await mongo_client.get_database().get_collection(collection).delete_many({})
       
@pytest.fixture
def product_id() -> UUID:
   return UUID("9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d")        
       
@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)       

@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)      
