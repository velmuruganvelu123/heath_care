import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from .routers import health

app = FastAPI(title="Healthcare Data API", version="1.0")

# Include routers
app.include_router(health.router,  tags=["Health"])

@app.get("/")
def home():
    return {"message": "API is running"}
