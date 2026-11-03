import os
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from errors import GearShareError, InvalidSKUError, ItemNotFoundError
from gearshare import GearShare
from storage.db import connect_database, initialize_database


def today_from_environment():
    return os.environ.get("TODAY", date.today().isoformat())


def build_service():
    connection = connect_database(":memory:")
    service = GearShare(connection=connection)
    service.load_data()
    return service


service = build_service()
TODAY = today_from_environment()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_service():
    return service


@app.exception_handler(GearShareError)
async def gearshare_error_handler(request, exc):
    status = 409
    if exc.prefix == "InvalidSKUError":
        status = 422
    elif exc.prefix in ("ItemNotFoundError", "CustomerNotFoundError"):
        status = 404
    message = exc.args[0] if exc.args else exc.default_message
    return JSONResponse(
        status_code=status,
        content={"error": exc.prefix, "message": message},
    )


class RentalRequest(BaseModel):
    customer_id: str
    sku: str


class WaitingListRequest(BaseModel):
    customer_id: str
    sku: str


class AddGearRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sku: str
    name: str
    tags: list[str] = []
    category: str
    item_type: str = "Equipment"
    weight_g: int = 0
    total: int = 1


def gear_json(item, gear_service):
    rented = sum(
        rental.return_date is None
        for rental in gear_service.rentals
        if rental.sku == item.sku
    )
    available = max(0, item.total_units - rented)
    return {
        "sku": item.sku,
        "name": item.name,
        "tags": item.tags.split(";") if item.tags else [],
        "category": item.category,
        "item_type": "Display" if item.__class__.__name__ == "DisplayItem" else
        "Accessory" if item.__class__.__name__ == "Accessory" else "Equipment",
        "available": available,
        "total": item.total_units,
        "weight_g": item.weight_g,
    }


@app.get("/gear")
def list_gear(
    q: str = "",
    category: str = "",
    sort: str = "name",
    gear_service: GearShare = Depends(get_service),
):
    items = gear_service.list_items()
    needle = q.lower()
    if needle:
        items = [
            item for item in items
            if needle in item.name.lower() or needle in item.tags.lower()
        ]
    if category:
        items = [
            item for item in items
            if item.category.lower() == category.lower()
            or item.parent_category.lower() == category.lower()
        ]
    if sort == "weight":
        items.sort(key=lambda item: item.weight_g)
    elif sort == "category":
        items.sort(key=lambda item: (item.category, item.name))
    else:
        items.sort(key=lambda item: item.name)
    return [gear_json(item, gear_service) for item in items]


@app.get("/gear/{sku}")
def get_gear(sku: str, gear_service: GearShare = Depends(get_service)):
    item = gear_service.items.get(sku)
    if item is None:
        raise ItemNotFoundError(sku)
    return gear_json(item, gear_service)


@app.post("/rentals", status_code=201)
def rent(payload: RentalRequest, gear_service: GearShare = Depends(get_service)):
    return gear_service.rent(payload.customer_id, payload.sku, TODAY)


@app.post("/rentals/{rental_id}/return")
def return_rental(rental_id: str, gear_service: GearShare = Depends(get_service)):
    result = gear_service.return_item(rental_id, TODAY)
    return {
        "rental_id": result["rental_id"],
        "days_late": result["days_late"],
        "fine": result["fee"],
        "next_in_waiting_list": result["next_in_waiting_list"],
    }


@app.post("/rentals/{rental_id}/extend")
def extend_rental(rental_id: str, gear_service: GearShare = Depends(get_service)):
    return gear_service.extend(rental_id, TODAY)


@app.post("/waiting-list")
def join_waiting(payload: WaitingListRequest, gear_service: GearShare = Depends(get_service)):
    position = gear_service.join_waiting_list(payload.customer_id, payload.sku)
    return {"position": position}


@app.get("/customers")
def list_customers(gear_service: GearShare = Depends(get_service)):
    return [
        {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "membership_type": customer.__class__.__name__.replace("Customer", ""),
            "max_items": customer.max_items(),
        }
        for customer in gear_service.customers.values()
    ]


@app.get("/customers/{customer_id}/rentals")
def customer_rentals(customer_id: str, gear_service: GearShare = Depends(get_service)):
    rentals = gear_service.customer_rentals(customer_id, TODAY)
    customer = gear_service.customers[customer_id]
    active = []
    for rental in rentals:
        if rental.return_date is None:
            due = gear_service._date(rental.due_date)
            today = gear_service._date(TODAY)
            days_overdue = max(0, (today - due).days)
            active.append({
                "rental_id": rental.rental_id,
                "item": gear_service.items[rental.sku].name,
                "due_date": gear_service._iso(rental.due_date),
                "days_overdue": days_overdue,
            })
    unpaid_fines = gear_service.unpaid_fines.get(customer_id, 0)
    return {
        "customer": customer.name,
        "membership_type": customer.__class__.__name__.replace("Customer", ""),
        "max_items": customer.max_items(),
        "unpaid_fines": unpaid_fines,
        "active": active,
    }


@app.post("/gear", status_code=201)
def add_gear(payload: AddGearRequest, gear_service: GearShare = Depends(get_service)):
    try:
        item = gear_service.add_item(
            payload.sku,
            payload.name,
            ";".join(payload.tags),
            payload.category,
            payload.item_type,
            payload.weight_g,
            0,
            payload.total,
        )
    except (InvalidSKUError, GearShareError) as exc:
        raise exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return gear_json(item, gear_service)
