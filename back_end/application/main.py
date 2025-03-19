import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import FastAPI
from .routers import health
from .routers import chatapi

app = FastAPI(title="Healthcare Data API", version="1.0")

# Include routers
app.include_router(health.router,  tags=["Health"])
app.include_router(chatapi.router, tags=['Chat'])


@app.get("/")
def home():
    return {"messa ge": "API is running"}
