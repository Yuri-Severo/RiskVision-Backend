from pydantic import BaseModel
from datetime import datetime

class RoleBase(BaseModel):
    description: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
