# app/core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup (no DB touch in Phase 1)
    yield
    # Shutdown
