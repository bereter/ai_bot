from contextlib import asynccontextmanager
import uvicorn
from core.config import settings, db_halper
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api_v1 import router as router_v1


origins = [
    "http://localhost",
    "http://localhost:8080",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_halper.dispose()


main_app = FastAPI(
    title='SpeechLand app',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


main_app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run('main:main_app', reload=True)
