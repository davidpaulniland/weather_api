from fastapi import FastAPI
from routes.metrics import router

app = FastAPI(title="Weather Sensor API")
app.include_router(router)
