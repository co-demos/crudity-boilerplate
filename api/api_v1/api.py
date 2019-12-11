from log_config import log_, pformat
from fastapi import APIRouter

from api.api_v1.endpoints import dataset_inputs, dataset_raws #, login, roles, users, utils

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(dataset_inputs.router, prefix="/dsi", tags=["dataset inputs"])
api_router.include_router(dataset_raws.router, prefix="/crud", tags=["dataset raws"])