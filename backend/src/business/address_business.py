import logging
from typing import List

from database.models import Address as AddressORM
from fastapi import HTTPException, status
from geopy.distance import geodesic
from helpers.common_log import CommonLog
from models.address import AddressCreate, AddressResponse, AddressUpdate
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class AddressBusiness:
    def create(self, session: Session, payload: AddressCreate) -> AddressResponse:
        logger.info(CommonLog.ADDRESS_CREATE_REQUEST)
        db_address = AddressORM(
            latitude=payload.latitude,
            longitude=payload.longitude,
            label=payload.label,
        )
        session.add(db_address)
        session.commit()
        session.refresh(db_address)
        logger.info(CommonLog.ADDRESS_CREATED)
        return AddressResponse.model_validate(db_address)

    def get_by_id(self, session: Session, address_id: int) -> AddressResponse:
        logger.info(CommonLog.ADDRESS_GET_REQUEST.format(id=address_id))
        db_address = session.get(AddressORM, address_id)
        if not db_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CommonLog.ADDRESS_NOT_FOUND,
            )
        return AddressResponse.model_validate(db_address)

    def list_all(self, session: Session) -> List[AddressResponse]:
        logger.info(CommonLog.ADDRESS_LIST_REQUEST)
        rows = session.query(AddressORM).order_by(AddressORM.id).all()
        return [AddressResponse.model_validate(row) for row in rows]

    def list_within_radius(
        self,
        session: Session,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> List[AddressResponse]:
        logger.info(CommonLog.ADDRESS_LIST_NEARBY_REQUEST)
        try:
            reference = (latitude, longitude)
            rows = session.query(AddressORM).order_by(AddressORM.id).all()
            result = []
            for row in rows:
                point = (row.latitude, row.longitude)
                distance_km = geodesic(reference, point).kilometers
                if distance_km <= radius_km:
                    result.append(AddressResponse.model_validate(row))
            return result
        except Exception as error:
            logger.exception(CommonLog.LIST_WITHIN_RADIUS_FAILED.format(error=error))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=CommonLog.INTERNAL_SERVER_ERROR,
            ) from error

    def update(
        self, session: Session, address_id: int, payload: AddressUpdate
    ) -> AddressResponse:
        logger.info(CommonLog.ADDRESS_UPDATE_REQUEST.format(id=address_id))
        db_address = session.get(AddressORM, address_id)
        if not db_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CommonLog.ADDRESS_NOT_FOUND,
            )
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_address, key, value)
        session.commit()
        session.refresh(db_address)
        logger.info(CommonLog.ADDRESS_UPDATED)
        return AddressResponse.model_validate(db_address)

    def delete(self, session: Session, address_id: int) -> None:
        logger.info(CommonLog.ADDRESS_DELETE_REQUEST.format(id=address_id))
        db_address = session.get(AddressORM, address_id)
        if not db_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CommonLog.ADDRESS_NOT_FOUND,
            )
        session.delete(db_address)
        session.commit()
        logger.info(CommonLog.ADDRESS_DELETED)
