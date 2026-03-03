from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    label: Optional[str] = Field(None, max_length=255, description="Optional label for the address")


class AddressUpdate(BaseModel):
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in degrees")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in degrees")
    label: Optional[str] = Field(None, max_length=255, description="Optional label for the address")


class AddressResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    label: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AddressListResponse(BaseModel):
    addresses: List[AddressResponse]


class NearbyQueryParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Reference latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Reference longitude in degrees")
    radius_km: float = Field(..., gt=0, description="Radius in kilometers")
