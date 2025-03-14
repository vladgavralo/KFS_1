from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Electricity Meter API")


app.include_router(router)


