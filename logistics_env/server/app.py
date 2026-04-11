from fastapi import FastAPI
from .routes import router as api_router

app = FastAPI(
    title="Logistics Optimizer API",
    description="API for the Logistics Optimizer RL Environment",
    version="1.0.0",
)

# ONLY THIS
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}



@app.get("/debug")
def debug():
    return [route.path for route in app.routes]