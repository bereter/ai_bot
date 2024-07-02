from fastapi import APIRouter

from .chats.views import router as chats_router

router = APIRouter()
router.include_router(router=chats_router, prefix='/chats')
