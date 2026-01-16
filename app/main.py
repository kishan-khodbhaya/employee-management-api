# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.employees import router as employees_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(employees_router)
app.include_router(auth_router)
app.include_router(health_router)
