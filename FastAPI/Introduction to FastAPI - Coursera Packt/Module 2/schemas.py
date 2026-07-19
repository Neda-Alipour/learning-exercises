from random import randint

from pydantic import BaseModel, Field

def random_destination():
    return randint(11000, 11999)

class Shipment(BaseModel):
    content: str = Field(max_length=100)
    weight: float = Field(description="Weight of the shipment in kg", le=25, ge=1)
    status: str = Field(description="Status of the shipment")
    destination: int | None = Field(description="Destination of the shipment", default_factory=random_destination)