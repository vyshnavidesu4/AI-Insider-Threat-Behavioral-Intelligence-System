from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import Base, engine
from app.routers.api_router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure all tables exist on startup (safety fallback if migrations have not executed)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"[Startup Warning] Could not auto-create tables: {exc}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SOC Behavioral Intelligence & Insider Threat Detection Engine for Regional Banking Operations",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware configuration
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "operational",
        "docs": "/docs",
        "api_prefix": settings.API_V1_STR,
    }
