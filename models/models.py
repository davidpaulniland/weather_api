from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class SensorData(BaseModel):
    sensor_id: str
    timestamp: datetime
    metrics: Dict[str, float]
