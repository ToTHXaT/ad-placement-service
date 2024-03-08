from pydantic import BaseModel


class OrmModel(BaseModel):
    class Config:
        from_attributes = True


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 100
