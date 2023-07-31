from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.proxies import ProxySchema, ProxySchemaAdd
from app.services.proxies import ProxiesService

router = APIRouter()


@router.post("/add_proxy", response_model=ProxySchema)
async def add_proxy(
    proxy: ProxySchemaAdd,
    proxies_service: ProxiesService = Depends(deps.proxies_service),
):
    return await proxies_service.add_proxy(proxy)
