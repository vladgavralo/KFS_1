from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import csv
import os
from app.database.db import get_db
from app.models.models import Meter, Reading, History
from app.services.calculator import calculate_cost
from config import AUTO_CORRECTION, TARIFFS
from pydantic import BaseModel

router = APIRouter()



class MeterCreate(BaseModel):
    meter_number: str
    owner_name: str


class ReadingCreate(BaseModel):
    meter_id: int
    day_kwh: float
    night_kwh: float


class TariffsUpdate(BaseModel):
    day_rate: float
    night_rate: float



@router.post("/add_meter")
def add_meter(meter: MeterCreate, db: Session = Depends(get_db)):
    existing_meter = db.query(Meter).filter(Meter.meter_number == meter.meter_number).first()
    if existing_meter:
        raise HTTPException(status_code=400, detail=" Лічильник вже існує!")

    new_meter = Meter(meter_number=meter.meter_number, owner_name=meter.owner_name)
    db.add(new_meter)
    db.commit()
    db.refresh(new_meter)
    return {"message": " Лічильник додано!", "meter_id": new_meter.id}



@router.post("/add_reading")
def add_reading(reading: ReadingCreate, db: Session = Depends(get_db)):
    meter = db.query(Meter).filter(Meter.id == reading.meter_id).first()
    if not meter:
        raise HTTPException(status_code=404, detail=" Лічильник не знайдено!")

    last_reading = db.query(Reading).filter(Reading.meter_id == reading.meter_id).order_by(Reading.date.desc()).first()

    if last_reading and (reading.day_kwh < last_reading.day_kwh or reading.night_kwh < last_reading.night_kwh):
        reading.day_kwh += AUTO_CORRECTION["day_kwh"]
        reading.night_kwh += AUTO_CORRECTION["night_kwh"]

    new_reading = Reading(meter_id=reading.meter_id, day_kwh=reading.day_kwh, night_kwh=reading.night_kwh)
    db.add(new_reading)
    db.commit()

    total_cost, day_cost, night_cost = calculate_cost(reading.day_kwh, reading.night_kwh)

    new_history = History(
        meter_id=reading.meter_id, day_kwh=reading.day_kwh, night_kwh=reading.night_kwh,
        day_cost=day_cost, night_cost=night_cost, total_cost=total_cost
    )
    db.add(new_history)
    db.commit()

    return {
        "message": " Показники збережено!",
        "total_cost": total_cost
    }



@router.get("/history")
def get_history(meter_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.meter_id == meter_id).order_by(History.date.desc()).all()
    if not history:
        raise HTTPException(status_code=404, detail=" Історію не знайдено!")
    return history



@router.put("/update_tariffs")
def update_tariffs(tariffs: TariffsUpdate):
    global TARIFFS
    TARIFFS["day_rate"] = tariffs.day_rate
    TARIFFS["night_rate"] = tariffs.night_rate
    return {"message": " Тарифи оновлено!", "new_tariffs": TARIFFS}



@router.get("/export_history")
def export_history(meter_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.meter_id == meter_id).order_by(History.date.desc()).all()

    if not history:
        raise HTTPException(status_code=404, detail=" Історію не знайдено!")

    filename = f"history_{meter_id}.csv"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Дата", "Денне споживання", "Нічне споживання", "Вартість (день)", "Вартість (ніч)", "Загальна вартість"])

        for row in history:
            writer.writerow([row.date, row.day_kwh, row.night_kwh, row.day_cost, row.night_cost, row.total_cost])

    return FileResponse(filepath, media_type="text/csv", filename=filename)
