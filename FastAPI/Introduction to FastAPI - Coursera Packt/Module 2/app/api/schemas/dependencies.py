from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated

from app.database.session import get_session

from app.services.shipment import ShipmentService


SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]