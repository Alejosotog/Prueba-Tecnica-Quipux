from fastapi import FastAPI

from api.routes.earthquakes import router as earthquakes_router
from api.routes.metrics import router as metrics_router
from api.routes.reports import router as reports_router


app = FastAPI(
    title="Quipux Earthquake API",
    description="API para procesamiento de eventos sísmicos en tiempo real",
    version="1.0.0"
)


app.include_router(earthquakes_router)
app.include_router(metrics_router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {
        "message": "Quipux Earthquake API funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }