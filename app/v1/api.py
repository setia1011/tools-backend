from fastapi import APIRouter
from app.v1.routers import home, file, quiz, install, user


router_v1 = APIRouter()
router_v1.include_router(home.router, prefix="", tags=["home"])
router_v1.include_router(install.router, prefix='/install', tags=['install'])
router_v1.include_router(user.router, prefix='/user', tags=['user'])
router_v1.include_router(file.router, prefix='/file', tags=['file'])
router_v1.include_router(quiz.router, prefix='/quiz', tags=['quiz'])