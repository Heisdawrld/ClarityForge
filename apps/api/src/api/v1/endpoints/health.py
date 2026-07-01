from fastapi import APIRouter

from monitoring.health import run_health_checks

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "clarityforge-api",
        "version": "1.0.0",
    }


@router.get("/health/detailed")
async def detailed_health_check():
    return await run_health_checks()


@router.get("/ready")
async def readiness_check():
    health = await run_health_checks()
    if health["status"] == "unhealthy":
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not ready")
    return {"status": "ready"}


@router.get("/metrics")
async def metrics():
    from monitoring.metrics import MetricsEndpoint
    return await MetricsEndpoint.get_summary()
