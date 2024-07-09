from fastapi import APIRouter

from .chats.views import router as chats_router
from .user.views import router as user_router

router = APIRouter()

router.include_router(router=chats_router, prefix='/chats')
router.include_router(router=user_router, prefix='/user')

