from fastapi.routing import APIRouter

from clips.web.api import clips

api_router = APIRouter()
api_router.include_router(clips.router, prefix="/clips", tags=["clips"])
