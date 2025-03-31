from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta

from models.models import SensorData
from utils.utils_io import load_data, save_data
from processing.processing import filter_and_aggregate

router = APIRouter()

@router.post("/metrics")
def add_sensor_data(data: SensorData):
    all_data = load_data()
    all_data.append(data.dict())
    save_data(all_data)
    return {"message": "Sensor data added"}

@router.get("/metrics")
def query_metrics(
    sensors: Optional[List[str]] = Query(None),
    metrics: List[str] = Query(...),
    stat: str = Query(..., pattern="^(min|max|sum|average)$"),
    start: Optional[datetime] = None,
    end: Optional[datetime] = None):

    if start and end:
        delta = end - start
        if delta < timedelta(days=1):
            raise HTTPException(status_code=400, detail="Date range must be at least 1 day.")
        if delta > timedelta(days=31):
            raise HTTPException(status_code=400, detail="Date range must be no more than 31 days.")

    data = load_data()
    return filter_and_aggregate(data, sensors, metrics, stat, start, end)
