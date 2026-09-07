from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/health", tags=["System Health"])


@router.get("", summary="Service health and database probe")
def health_check(db: Session = Depends(get_db)):
    """Check backend service liveness and database connectivity."""
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "online",
        "service": "insider-threat-backend",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.1.0",
    }
