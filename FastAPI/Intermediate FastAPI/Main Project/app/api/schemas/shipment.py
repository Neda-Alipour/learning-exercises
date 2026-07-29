from datetime import datetime
from random import randint

from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus


def random_destination():
    return randint(11000, 11999)

class BaseShipment(BaseModel):
    content: str = Field(max_length=100)
    weight: float = Field(description="Weight of the shipment in kg", le=25, ge=1)
    destination: int | None = Field(description="Destination of the shipment", default_factory=random_destination)


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)

# we can also create a separate Order model and include it in the ShipmentCreate model as a nested model. This way, we can validate the order data separately and ensure that it is included in the shipment data.
# class Order(BaseModel):
#     price: int
#     title: str

# class ShipmentCreate(BaseShipment):
#     order: Order