from fastapi import FastAPI

from city_app.router import router as city_router
from temperature_app.router import router as temperature_router

app = FastAPI()

app.include_router(city_router, prefix="/api")
app.include_router(temperature_router, prefix="/api")


@app.get("/api/")
def root():
    return {"message": "It is the main root"}
