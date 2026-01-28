from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    # Enables Pydantic to parse data directly from ORM model attributes (e.g., post.id) 
    # instead of requiring a standard Python dictionary (e.g., post["id"])
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_posted: str
