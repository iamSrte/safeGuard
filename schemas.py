import enum
from datetime import date, time
from pydantic import BaseModel, Field
from typing import Optional


class Gender(str, enum.Enum):
    F = 'F'
    M = 'M'


class PassengerBase(BaseModel):
    passenger_id: str = Field(..., pattern='^[0-9]{9}$')
    passport: str = Field(..., pattern='^[0-9]{9}$')
    first_name: str = Field(..., pattern='^[a-zA-Z''-]+$', max_length=20)
    last_name: str = Field(..., pattern='^[a-zA-Z''-]+$', max_length=20)
    sex: Gender
    birthdate: date
    phone_number: str = Field(..., pattern='^[0-9]{11}$')
    email_address: Optional[str] = Field(..., pattern='^[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$')
    country: str = Field(..., pattern='^[a-zA-Z0-9''&(),. -]+$', max_length=100)
    city: str = Field(..., pattern='^[a-zA-Z''&() -]+$', max_length=100)
    street: str = Field(..., pattern='^[a-zA-Z0-9''&(),. -]+$', max_length=255)
    zip_code: str = Field(..., pattern='^[0-9]{10}$')

    class Config:
        from_attributes = True


class OutgoingFlightBase(BaseModel):
    flight_number: str = Field(..., pattern='^[A-Z0-9]{7}$')
    to_country: str = Field(..., pattern='^[a-zA-Z0-9''&(),. -]+$', max_length=100)
    to_city: str = Field(..., pattern='^[a-zA-Z''&() -]+$', max_length=100)
    departure_date: date
    departure_time: time
    arrival_date: date
    arrival_time: time

    class Config:
        from_attributes = True


class ItemActionBase(BaseModel):
    action_id: str = Field(..., pattern=r'^[0-9]{4}$')
    description: str

    class Config:
        from_attributes = True


class ForbiddenItemBase(BaseModel):
    item_id: str = Field(..., pattern='^[0-9]{4}$')
    name: str = Field(..., pattern='^[a-zA-Z0-9''., -]+$', max_length=20)
    description: Optional[str] = None
    action_id: str = Field(..., pattern='^[0-9]{4}$')

    class Config:
        from_attributes = True


class BaggageScanBase(BaseModel):
    scan_id: str = Field(..., pattern='^[0-9]{10}$')
    date: date
    time: time
    flight_number: str = Field(..., pattern='^[A-Z0-9]{7}$')
    passenger_id: str = Field(..., pattern='^[0-9]{9}$')

    class Config:
        from_attributes = True


class ScanItemBase(BaseModel):
    scan_id: str = Field(..., pattern='^[0-9A-Z]{10}$')
    item_id: str = Field(..., pattern='^[0-9]{4}$')
    quantity: int

    class Config:
        from_attributes = True
