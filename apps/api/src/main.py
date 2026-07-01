import logging
import sys
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import router as v1_router
from config import settings
from db.database import engine
from middleware.cache import CacheMiddleware
from middleware.error_handler import add_error_handlers
from middleware.logging import LoggingMiddleware
from middleware.rate_limit import RateLimitMiddleware
from middleware.security import SecurityMiddleware

# Sentry initialization
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.1,
        environment=settings.ENVIRONMENT,
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.info("Starting ClarityForge API...")
    yield
    # Shutdown
    logging.info("Shutting down ClarityForge API...")
    await engine.dispose()


app = FastAPI(
    title="ClarityForge API",
    description="AI-powered thinking partner that audits cognitive biases and tracks judgment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Security headers (first, outermost)
app.add_middleware(SecurityMiddleware)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)

# Caching (last, innermost)
app.add_middleware(CacheMiddleware)

# Error handlers
add_error_handlers(app)

# API routes
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
