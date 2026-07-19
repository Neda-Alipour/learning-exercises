from enum import Enum

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from .schemas import Shipment

app = FastAPI()

shipments = {
    15656: {"weight": 2.2, "content": "Glass", "status": "placed"},
    15657: {"weight": 5.0, "content": "Books", "status": "shipped"},
    15658: {"weight": 8.3, "content": "Ceramics", "status": "delivered"},
    15659: {"weight": 1.1, "content": "Electronics", "status": "pending"},
    15660: {"weight": 12.5, "content": "Furniture", "status": "in transit"},
    15661: {"weight": 0.9, "content": "Jewelry", "status": "picked up"},
    15662: {"weight": 4.7, "content": "Clothing", "status": "processing"},
}


# Registering fixed routes before dynamic parameter routes ensures correct request handling and prevents unintended errors
@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment")
    # instead of returning a dictionary, we can return a Pydantic model instance
def get_shipment(id: int) -> Shipment:

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist in the shipment records",
        )
    shipment = shipments[id]

    # instead of Shipment(content=shipment["content"], weight=shipment["weight"], status=shipment["status"]) we can unpack the shipment dictionary and pass it to the Shipment model constructor using the ** operator
    return Shipment(**shipment)


# @app.get("/shipment/{id}")
# def get_shipment(id: int) -> dict[str, Any]:

#     if id not in shipments:
#         return {"error": "Shipment not found"}

#     return shipments[id]


@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:
    weight = shipment.weight
    content = shipment.content
    status = shipment.status
    destination = shipment.destination

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": weight,
        "content": content,
        "status": status,
        "destination": destination,
    }
    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}


@app.put("/shipment")
def shipment_update(id: int, shipment: Shipment) -> dict[str, Any]:
    shipments[id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "status": shipment.status,
    }
    return shipments[id]


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


@app.patch("/shipment")
def patch_shipment(id: int, body: dict[str, ShipmentStatus]) -> dict[str, Any]:

    shipment = shipments[id]

    shipment.update(body)

    shipments[id] = shipment

    return shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, Any]:
    shipments.pop(id)
    return {"message": "Shipment deleted successfully"}


# Scalar API Documentation endpoint
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
