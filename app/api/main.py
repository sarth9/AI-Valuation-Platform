from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.predictor_public import public_model_service
from app.api.routes_private import router as private_router
from app.api.routes_public import router as public_router
from app.api.routes_startup import router as startup_router
from app.core.config import settings
from app.core.logger import setup_logger


logger = setup_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    public_model_service.load_artifacts()
    logger.info("Application startup complete.")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-mode AI valuation platform for public companies, private companies, and startups/SaaS.",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running",
        "status": "ok",
        "modes": ["public_company", "private_company", "startup_saas"],
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "public_model_loaded": public_model_service.model is not None,
        "version": settings.APP_VERSION,
    }


app.include_router(public_router)
app.include_router(private_router)
app.include_router(startup_router)