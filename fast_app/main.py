from contextlib import asynccontextmanager
import uvicorn
from core.models import Base, db_halper
from core.config import settings
from fastapi import FastAPI

from api_v1 import router as router_v1
# from items_views import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_halper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title='SpeechLand app', lifespan=lifespan)
# app.include_router(items_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
