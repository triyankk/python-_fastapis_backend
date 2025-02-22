from fastapi import APIRouter, Depends
from ....api import deps
from ....models.user import User
from ....monitoring.prometheus import metrics
import psutil
import platform

router = APIRouter()

@router.get("/metrics")
async def get_metrics(current_user: User = Depends(deps.check_admin_access)):
    return await metrics()

@router.get("/system")
async def get_system_info(current_user: User = Depends(deps.check_admin_access)):
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "platform": platform.platform(),
        "python_version": platform.python_version()
    }
