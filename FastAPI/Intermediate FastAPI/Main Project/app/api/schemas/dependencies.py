from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated

from app.database.session import get_session

from app.services.seller import SellerService
from app.services.shipment import ShipmentService


SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)


ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

