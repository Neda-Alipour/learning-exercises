from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID

from pydantic import EmailStr
from sqlmodel import Column, Field, SQLModel, Relationship
from sqlalchemy.dialects import postgresql


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    # when defining a custom column type, we need to use the sa_column parameter of the Field class to specify the column type. In this case, we are using the postgresql.UUID type for the id field.
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            primary_key=True,
            default=uuid4,
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    # seller.id is the table name
    seller_id: UUID = Field(foreign_key="seller.id")
    # instead of session.get(Seller, shipment.seller_id) we can use this to get the seller object directly from the shipment object
    seller: "Seller" = Relationship(
        back_populates="shipments",
        # to avoid lazy loading and get the seller object when we get the shipment object, we can use selectin loading
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Seller(SQLModel, table=True):
    # we can skip table name because it has default name of the class (Seller)

    id: UUID = Field(
            sa_column=Column(
                postgresql.UUID,
                primary_key=True,
                default=uuid4,
            )
        )
    name: str

    email: EmailStr
    password_hash: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
