from fastapi import APIRouter

from helpers.api_paths import ApiPaths
from helpers.common_log import CommonLog

router = APIRouter()

@router.get(ApiPaths.HEALTH)
def health():
    return {"status": CommonLog.SUCCESS}
