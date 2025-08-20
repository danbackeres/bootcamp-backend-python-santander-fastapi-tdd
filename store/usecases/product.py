from uuid import UUID
from motor.motor.asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client
from pydantic import BaseModel
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUdateOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import BaseException, NotFoundException
import pymongo

class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")
        
    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())
        return ProductOut(**product_model.model_dump())
    
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
    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message="Product not found")
        result = await self.collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False
        
product_usecase = ProductUseCase()