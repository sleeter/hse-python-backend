from fastapi import APIRouter, Response, Query
from typing import Optional
from hw_2.models.models import ItemCreateRequest, ItemPutRequest, ItemPatchRequest
import hw_2.services.item as itemService
from http import HTTPStatus

router = APIRouter(prefix="/item")


@router.post("/", status_code=HTTPStatus.CREATED)
async def post_item(req: ItemCreateRequest, response: Response):
    item = await itemService.create_item(req)
    response.headers["location"] = f"/item/{item.id}"
    return item

@router.get("/{item_id}")
async def get_item(item_id: int):
    item = await itemService.get_item_by_id(item_id)
    return item


@router.get("/")
async def get_items(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0.0),
    max_price: Optional[float] = Query(None, ge=0.0),
    show_deleted: bool = Query(False),
):
    items = await itemService.get_items(offset, limit, min_price, max_price, show_deleted)
    return items


@router.put("/{item_id}")
async def put_item(item_id: int, item: ItemPutRequest):
    item = await itemService.put_item(item_id, item)
    return item

@router.patch("/{item_id}")
async def patch_item(item_id: int, item: ItemPatchRequest):
    item = await itemService.patch_item(item_id, item)
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    resp = itemService.delete_item(item_id)
    return resp