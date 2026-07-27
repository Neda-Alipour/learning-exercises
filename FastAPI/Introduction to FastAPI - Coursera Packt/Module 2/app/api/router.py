from fastapi import APIRouter

router = APIRouter()


@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id: int, session: SessionDep):
    
    shipment = await session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist in the shipment records",
        )
    

    # instead of Shipment(content=shipment["content"], weight=shipment["weight"], status=shipment["status"]) we can unpack the shipment dictionary and pass it to the Shipment model constructor using the ** operator
    # return Shipment(**shipment)

    # or better way to do this is instead of def get_shipment(id: int) -> Shipment: we can write @app.get("/shipment", response_model=Shipment) and then return the shipment dictionary directly without creating a Shipment instance
    return shipment


@router.post("/shipment")
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, Any]:

    # new_id = max(shipments.keys()) + 1

    # # we can also use the model_dump() method to convert the Pydantic model instance to a dictionary and then update the shipments dictionary with the new shipment data. This way, we can validate the data and ensure that it is in the correct format before adding it to the shipments dictionary.
    # shipments[new_id] = {
    #     # "weight": weight,
    #     # "content": content,
    #     # "status": status,
    #     **shipment.model_dump(),  # This will validate the data and raise a ValidationError if any field is invalid
    #     "status": "placed",
    # }
    
    
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now(timezone.utc) + timedelta(days=3)
    )

    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


@router.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):

    # why we need to use model_dump() is because we want to convert the Pydantic model instance to a dictionary so that we can update the shipments dictionary with the new shipment data. The model_dump() method will validate the data and raise a ValidationError if any field is invalid. This way, we can ensure that the data is in the correct format before updating the shipments dictionary.
    # why we need to use model_dump(exclude_unset=True) is because we want to update only the fields that are provided in the request body. If we don't use exclude_unset=True, then all the fields in the ShipmentUpdate model will be included in the dictionary, even if they are not provided in the request body. This can lead to overwriting existing values with None or default values, which is not what we want. By using exclude_unset=True, we ensure that only the fields that are explicitly set in the request body are included in the dictionary, and the existing values for other fields remain unchanged.
    # shipments[id].update(body.model_dump(exclude_unset=True))

    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update."
        )

    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist in the shipment records",
        )
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@router.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    # shipments.pop(id)
    
    session.delete(
        session.get(Shipment, id)
    )
    session.commit()

    return {"message": "Shipment deleted successfully"}



# Registering fixed routes before dynamic parameter routes ensures correct request handling and prevents unintended errors
# @app.get("/shipment/latest")
# def get_latest_shipment() -> dict[str, Any]:
#     id = max(shipments.keys())
#     return shipments[id]

# @app.get("/shipment/{field}")
# def get_shipment_field(field: str, id: int) -> dict[str, Any]:
#     return {field: shipments[id][field]}

# @app.put("/shipment")
# def shipment_update(id: int, shipment: Shipment) -> dict[str, Any]:
#     shipments[id] = {
#         "weight": shipment.weight,
#         "content": shipment.content,
#         "status": shipment.status,
#     }
#     return shipments[id]


# @app.get("/shipment/{id}")
# def get_shipment(id: int) -> dict[str, Any]:

#     if id not in shipments:
#         return {"error": "Shipment not found"}

#     return shipments[id]