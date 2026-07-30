from fastapi import FastAPI
from app.config.settings import settings
from app.api.routers import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
)

# Register root route
@app.get("/")
def read_root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "running"
    }

# Register sub-routers
app.include_router(api_router, prefix=settings.API_V1_STR)
