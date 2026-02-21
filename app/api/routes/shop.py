from fastapi import APIRouter, Depends, Response
from app.core.dependencies import require_admin
from app.schemas.pagination import PaginatedParams, PaginatedResponse
from app.schemas.shop import ShopItemCreate, ShopItemResponse, ShopItemUpdate
from app.services.shop import ShopService, get_shop_items_service


router = APIRouter(prefix="/shop")
shop_tag = ["Магазин"]


@router.get("/items", tags=shop_tag)
async def get_items(
    service: ShopService = Depends(get_shop_items_service),
    params: PaginatedParams = Depends(),
) -> PaginatedResponse:
    return await service.get_shop_items(params)


@router.post("/items", tags=shop_tag)
async def create_item(
    item: ShopItemCreate,
    service: ShopService = Depends(get_shop_items_service),
    _: None = Depends(require_admin),
) -> ShopItemResponse:
    new_item = await service.create_shop_item(item)
    return ShopItemResponse.model_validate(new_item)


@router.delete("/items/{item_id}", tags=shop_tag)
async def delete_item(
    item_id: int,
    service: ShopService = Depends(get_shop_items_service),
    _: None = Depends(require_admin),
):
    await service.delete_shop_item(item_id)
    return Response(status_code=204)


@router.patch("/items/{item_id}", tags=shop_tag)
async def update_item(
    item_id: int,
    item: ShopItemUpdate,
    service: ShopService = Depends(get_shop_items_service),
    _: None = Depends(require_admin),
) -> ShopItemResponse:
    updated_item = await service.update_shop_item(item_id, item)
    return ShopItemResponse.model_validate(updated_item)