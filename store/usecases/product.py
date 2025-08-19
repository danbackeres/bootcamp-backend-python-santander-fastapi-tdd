from uuid import UUID
from motor.motor.asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client
from pydantic import BaseModel
from store.schemas.product import ProductIn, ProductOut, ProductUdateOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import BaseException, NotFoundException
import pymongo

class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")
        
    async def create(self, body: ProductIn) -> ProductOut:
        product = ProductOut(**body.model_dump())
        await self.collection.insert_one(product.model_dump())
        return product
    
    async def get(self, id: UUID) -> ProductOut:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message="Product not found")
        return ProductOut(**product)
    
    async def query(self, limit: int) -> list[ProductOut]:
        await [ProductOut(**item) async for item in self.collection.find().limit(limit)]
        
    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER
        )
        return ProductUpdateOut(**result)
        
product_usecase = ProductUseCase()