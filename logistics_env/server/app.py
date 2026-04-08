from fastapi import FastAPI
from .routes import router as api_router

app = FastAPI(
    title="Logistics Optimizer API",
    description="API for the Logistics Optimizer RL Environment",
    version="1.0.0",
)

app.include_router(api_router)
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
