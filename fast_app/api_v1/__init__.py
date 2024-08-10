from fastapi import APIRouter

from api_v1.views import router_user, router_chats

router = APIRouter()

router.include_router(router=router_chats, prefix='/chat')
router.include_router(router=router_user, prefix='/account')

