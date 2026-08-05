from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Annotated

from app.database.models import Seller
from app.database.session import get_session

from app.services.seller import SellerService
from app.services.shipment import ShipmentService

from app.core.security import oauth2_scheme
from app.utils import decode_access_token

from app.database.redis import is_jti_blacklisted


SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)

# Access token data dep
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    data = decode_access_token(token)
    
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )

    return data
    
# Logged in seller
async def get_current_seller(token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep) -> Seller:

    return await session.get(Seller, UUID(token_data["user"]["id"]))

# Seller dep
SellerDep = Annotated[
    Seller,
    Depends(get_current_seller)
]

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

