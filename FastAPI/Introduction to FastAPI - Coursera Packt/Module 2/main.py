from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()

shipments = {
     15656: {
        "weight": 2.2,
        "content": "Glass",
        "status": "placed"
    },
    15657: {
        "weight": 5.0,
        "content": "Books",
        "status": "shipped"
    },
    15658: {
        "weight": 8.3,
        "content": "Ceramics",
        "status": "delivered"
    },
    15659: {
        "weight": 1.1,
        "content": "Electronics",
        "status": "pending"
    },
    15660: {
        "weight": 12.5,
        "content": "Furniture",
        "status": "in transit"
    },
    15661: {
        "weight": 0.9,
        "content": "Jewelry",
        "status": "picked up"
    },
    15662: {
        "weight": 4.7,
        "content": "Clothing",
        "status": "processing"
    },
}


# Registering fixed routes before dynamic parameter routes ensures correct request handling and prevents unintended errors
@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment")
def get_shipment(id: int) -> dict[str, Any]:
    
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Given id does not exist in the shipment records"
            )
    
    return shipments[id]

# @app.get("/shipment/{id}")
# def get_shipment(id: int) -> dict[str, Any]:

#     if id not in shipments:
#         return {"error": "Shipment not found"}
    
#     return shipments[id]

@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, Any]:

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="Weight exceeds the maximum limit of 25kg"
            )

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": weight, 
        "content": content, 
        "status": "placed"
    }
    return {"id": new_id}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )