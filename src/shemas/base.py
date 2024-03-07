from pydantic import BaseModel


class OrmModel(BaseModel):
    class Config:
        from_attributes = True
