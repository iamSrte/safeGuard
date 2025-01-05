import enum
from db import Base
from sqlalchemy import Column, ForeignKey, CheckConstraint, String, CHAR, Date, Time, Enum, Integer
from sqlalchemy.orm import relationship


class Gender(enum.Enum):
    F = 'F'
    M = 'M'


class Passenger(Base):
    __tablename__ = 'passengers'
    __table_args__ = (
        CheckConstraint("passenger_id ~ '^[0-9]{9}$'"),
        CheckConstraint("passport ~ '^[0-9]{9}$'"),
        CheckConstraint("phone_number ~ '^[0-9]{11}$'"),
        CheckConstraint("email_address ~ '^[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'"),
        CheckConstraint("country ~ '^[a-zA-Z0-9''&(),.- ]+$'"),
        CheckConstraint("city ~ '^[a-zA-Z''&()- ]+$'"),
        CheckConstraint("street ~ '^[a-zA-Z0-9''&(),.- ]+$'"),
        CheckConstraint("zip_code ~ '^[0-9]{10}$'"),
        CheckConstraint("first_name ~ '^[a-zA-Z''-]+$' AND last_name ~ '^[a-zA-Z''-]+$'"),
    )
    passenger_id = Column(CHAR(9), nullable=False, primary_key=True)
    passport = Column(CHAR(9), nullable=False, unique=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    sex = Column(Enum(Gender), nullable=False)
    birthdate = Column(Date, nullable=False)
    phone_number = Column(String(11), nullable=False)
    email_address = Column(String(320), nullable=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    street = Column(String(255), nullable=False)
    zip_code = Column(CHAR(10), nullable=False)


class OutgoingFlight(Base):
    __tablename__ = 'outgoing_flights'
    __table_args__ = (
        CheckConstraint("flight_number ~ '^[A-Z0-9]{7}$'"),
        CheckConstraint("to_country ~ '^[a-zA-Z0-9''&(),.- ]+$'"),
        CheckConstraint("to_city ~ '^[a-zA-Z''&()- ]+$'"),
    )

    flight_number = Column(CHAR(7), primary_key=True)
    to_country = Column(String(100), nullable=False)
    to_city = Column(String(100), nullable=False)
    departure_date = Column(Date)
    departure_time = Column(Time)
    arrival_date = Column(Date)
    arrival_time = Column(Time)


class ItemAction(Base):
    __tablename__ = 'item_actions'
    __table_args__ = (
        CheckConstraint("action_id ~ '^[0-9]{4}$'"),
    )

    action_id = Column(CHAR(4), primary_key=True)
    description = Column(String(225))


class ForbiddenItem(Base):
    __tablename__ = 'forbidden_items'
    __table_args__ = (
        CheckConstraint("item_id ~ '^[0-9]{4}$'"),
        CheckConstraint("name ~ '^[a-zA-Z0-9''.,- ]+$'"),
    )

    item_id = Column(CHAR(4), primary_key=True)
    name = Column(String(20), nullable=False)
    description = Column(String(225))
    action_id = Column(CHAR(4), ForeignKey('item_actions.action_id'))
    # scans = relationship('BaggageScan', back_populates='forbidden')


class BaggageScan(Base):
    __tablename__ = 'baggage_scans'
    __table_args__ = (
        CheckConstraint("scan_id ~ '^[0-9]{10}$'"),
    )

    scan_id = Column(CHAR(10), primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    flight_number = Column(CHAR(7), ForeignKey('outgoing_flights.flight_number'), nullable=False)
    passenger_id = Column(CHAR(9), ForeignKey('passengers.passenger_id'), nullable=False)
    # forbidden = relationship('ForbiddenItem', back_populates='scans')
    # items = relationship('ScanItem', back_populates='scans')


class ScanItem(Base):
    __tablename__ = 'scan_items'
    scan_id = Column(CHAR(10), ForeignKey('baggage_scans.scan_id'), nullable=False, primary_key=True)
    item_id = Column(CHAR(4), ForeignKey('forbidden_items.item_id'), nullable=False, primary_key=True)
    quantity = Column(Integer, nullable=False)
    # scans = relationship('BaggageScan', back_populates='items')
