from pydantic import BaseModel, UUID4, Field
import uuid
from datetime import datetime

class BaseSchemaMixin(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)