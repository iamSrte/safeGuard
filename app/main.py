from sqlalchemy import func, delete, update
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends, HTTPException
from typing import Annotated, Optional

from app.db import engine, SessionLocal, Base
from app.models import Passenger, OutgoingFlight, ItemAction, ForbiddenItem, BaggageScan, ScanItem
from app.schemas import PassengerBase, OutgoingFlightBase, ItemActionBase, ForbiddenItemBase, BaggageScanBase, ScanItemBase

app = FastAPI()
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='app/templates')
app.mount('/style', StaticFiles(directory='app/style'), name='style')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/')
async def root(
        request: Request, db: db_dependency,
        scan_id: Optional[str] = None,
        pass_name: Optional[str] = None,
        passport_num: Optional[str] = None
):
    status = db.query(ScanItem).filter(ScanItem.scan_id == BaggageScan.scan_id).exists()
    query = db.query(
        BaggageScan.scan_id,
        Passenger.first_name,
        Passenger.last_name,
        Passenger.passport,
        BaggageScan.date,
        BaggageScan.time,
        status
    )
    query = query.filter(BaggageScan.passenger_id == Passenger.passenger_id)
    query = query.order_by(BaggageScan.date.desc(), BaggageScan.time.desc())
    if scan_id:
        query = query.filter(BaggageScan.scan_id.ilike(f'%{scan_id}%'))
    if pass_name:
        query = query.filter(func.concat(Passenger.first_name, ' ', Passenger.last_name).ilike(f'%{pass_name}%'))
    if passport_num:
        query = query.filter(Passenger.passport.ilike(f'%{passport_num}%'))
    results = query.all()

    return templates.TemplateResponse(
        'log_page.html', {
            'request': request,
            'scans': results,
            'params': {
                'scan_id': scan_id,
                'pass_name': pass_name,
                'passport_num': passport_num
            }
        }
    )


@app.get('/scan/{scan_id}')
async def scan(db: db_dependency, scan_id):
    query = db.query(
        BaggageScan.scan_id,
        BaggageScan.date,
        BaggageScan.time,
        BaggageScan.flight_number,
        Passenger.first_name,
        Passenger.last_name,
        Passenger.passport,
    ).filter(BaggageScan.scan_id == scan_id).filter(BaggageScan.passenger_id == Passenger.passenger_id)
    query = query.all()

    if not query:
        raise HTTPException(status_code=404, detail='Item not found')

    response = {
        'scan_id': query[0][0],
        'data': query[0][1],
        'time': query[0][2],
        'flight_number': query[0][3],
        'first_name': query[0][4],
        'last_name': query[0][5],
        'passport': query[0][6],
        'items_found': {}
    }
    query = db.query(ForbiddenItem.name).filter(ScanItem.scan_id == scan_id).filter(
        ForbiddenItem.item_id == ScanItem.item_id)
    print(query.all())
    for i, item in enumerate(query):
        response['items_found'][i] = item[0]
    return response


@app.post('/add_passenger')
async def add_passenger(passenger: PassengerBase, db: db_dependency):
    db_passenger = Passenger(
        passenger_id=passenger.passenger_id,
        passport=passenger.passport,
        first_name=passenger.first_name,
        last_name=passenger.last_name,
        sex=passenger.sex,
        birthdate=passenger.birthdate,
        phone_number=passenger.phone_number,
        email_address=passenger.email_address,
        country=passenger.country,
        city=passenger.city,
        street=passenger.street,
        zip_code=passenger.zip_code
    )
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)


@app.post('/add_outgoing_flight')
async def add_outgoing_flight(flight: OutgoingFlightBase, db: db_dependency):
    db_flight = OutgoingFlight(
        flight_number=flight.flight_number,
        to_country=flight.to_country,
        to_city=flight.to_city,
        departure_date=flight.departure_date,
        departure_time=flight.departure_time,
        arrival_date=flight.arrival_date,
        arrival_time=flight.arrival_time
    )
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)


@app.post('/add_item_action')
async def add_item_action(action: ItemActionBase, db: db_dependency):
    db_item_action = ItemAction(
        action_id=action.action_id,
        description=action.description
    )
    db.add(db_item_action)
    db.commit()
    db.refresh(db_item_action)


@app.post('/add_forbidden_item')
async def add_forbidden_item(item: ForbiddenItemBase, db: db_dependency):
    db_forbidden_item = ForbiddenItem(
        item_id=item.item_id,
        name=item.name,
        description=item.description,
        action_id=item.action_id
    )
    db.add(db_forbidden_item)
    db.commit()
    db.refresh(db_forbidden_item)


@app.post('/add_scan_record')
async def add_scan_record(scan_record: BaggageScanBase, db: db_dependency):
    db_scan_record = BaggageScan(
        scan_id=scan_record.scan_id,
        date=scan_record.date,
        time=scan_record.time,
        flight_number=scan_record.flight_number,
        passenger_id=scan_record.passenger_id,
    )
    db.add(db_scan_record)
    db.commit()
    db.refresh(db_scan_record)


@app.post('/add_scan_item')
async def add_scan_item(scan_item: ScanItemBase, db: db_dependency):
    db_scan_item = ScanItem(
        scan_id=scan_item.scan_id,
        item_id=scan_item.item_id,
        quantity=scan_item.quantity
    )
    db.add(db_scan_item)
    db.commit()
    db.refresh(db_scan_item)


@app.post('/remove_scan_item')
async def remove_scan_item(scan_id, item_id, db: db_dependency):
    query = (
        delete(ScanItem)
        .where(ScanItem.scan_id == scan_id)
        .where(ScanItem.item_id == item_id)
    )
    if db.execute(query).rowcount == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    db.commit()
    return {'Item removed'}


@app.post('/change_item_quantity')
async def change_item_quantity(scan_id, item_id, quantity: int, db: db_dependency):
    query = (
        update(ScanItem)
        .where(ScanItem.scan_id == scan_id)
        .where(ScanItem.item_id == item_id)
        .values(quantity=quantity)
    )
    if db.execute(query).rowcount == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    db.commit()
    return {'Item updated'}
