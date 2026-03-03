from typing import List, Optional

from business.address_business import AddressBusiness
from helpers.common_log import CommonLog
from models.address import AddressCreate, AddressResponse, AddressUpdate
from sqlalchemy.orm import Session


address_business = AddressBusiness()


def create_address_controller(session: Session, payload: AddressCreate) -> dict:
    result = address_business.create(session, payload)
    return {"detail": CommonLog.ADDRESS_CREATED, "address": result.model_dump()}


def get_address_controller(session: Session, address_id: int) -> AddressResponse:
    return address_business.get_by_id(session, address_id)


def list_addresses_controller(
    session: Session,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = None,
) -> List[AddressResponse]:
    if latitude is not None and longitude is not None and radius_km is not None:
        return address_business.list_within_radius(session, latitude, longitude, radius_km)
    return address_business.list_all(session)


def update_address_controller(
    session: Session, address_id: int, payload: AddressUpdate
) -> dict:
    result = address_business.update(session, address_id, payload)
    return {"detail": CommonLog.ADDRESS_UPDATED, "address": result.model_dump()}


def delete_address_controller(session: Session, address_id: int) -> None:
    address_business.delete(session, address_id)
