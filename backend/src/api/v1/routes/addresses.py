from typing import Optional

from controllers.address_controller import (
    create_address_controller,
    delete_address_controller,
    get_address_controller,
    list_addresses_controller,
    update_address_controller,
)
from fastapi import APIRouter, Depends, Query, status
from helpers.api_paths import ApiPaths
from models.address import AddressCreate, AddressResponse, AddressUpdate
from database.session import get_session
from sqlalchemy.orm import Session


router = APIRouter()


@router.post(ApiPaths.ADDRESSES, status_code=status.HTTP_201_CREATED)
def create_address(
    payload: AddressCreate,
    db: Session = Depends(get_session),
):
    return create_address_controller(db, payload)


@router.get(ApiPaths.ADDRESSES, response_model=list[AddressResponse])
def list_addresses(
    latitude: Optional[float] = Query(None, ge=-90, le=90),
    longitude: Optional[float] = Query(None, ge=-180, le=180),
    radius_km: Optional[float] = Query(None, gt=0),
    db: Session = Depends(get_session),
):
    return list_addresses_controller(db, latitude, longitude, radius_km)


@router.get(ApiPaths.ADDRESS_BY_ID, response_model=AddressResponse)
def get_address(
    id: int,
    db: Session = Depends(get_session),
):
    return get_address_controller(db, id)


@router.patch(ApiPaths.ADDRESS_BY_ID, response_model=dict)
def update_address(
    id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_session),
):
    return update_address_controller(db, id, payload)


@router.delete(ApiPaths.ADDRESS_BY_ID, status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    id: int,
    db: Session = Depends(get_session),
):
    delete_address_controller(db, id)
    return None
