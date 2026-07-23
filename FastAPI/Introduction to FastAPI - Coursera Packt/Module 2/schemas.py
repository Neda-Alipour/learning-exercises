from enum import Enum
from random import randint

from pydantic import BaseModel, Field

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


def random_destination():
    return randint(11000, 11999)

class BaseShipment(BaseModel):
    content: str = Field(max_length=100)
    weight: float = Field(description="Weight of the shipment in kg", le=25, ge=1)
    destination: int | None = Field(description="Destination of the shipment", default_factory=random_destination)


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str | None= Field(default=None)
    weight: float | None = Field(default=None)
    destination: int | None = Field(default=None)
    status: ShipmentStatus

# we can also create a separate Order model and include it in the ShipmentCreate model as a nested model. This way, we can validate the order data separately and ensure that it is included in the shipment data.
# class Order(BaseModel):
#     price: int
#     title: str

# class ShipmentCreate(BaseShipment):
#     order: Order