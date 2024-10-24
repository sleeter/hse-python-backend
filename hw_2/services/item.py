from typing import Dict, List
from hw_2.models.models import Item, ItemPutRequest, ItemPatchRequest, ItemCreateRequest
from fastapi import HTTPException
from http import HTTPStatus

items_db: Dict[int, Item] = {}
item_id_counter = 0

async def create_item(req: ItemCreateRequest) -> Item:
    global item_id_counter
    item = Item(id=item_id_counter, name=req.name, price=req.price)
    items_db[item_id_counter] = item
    item_id_counter += 1
    return item

async def get_item_by_id(id: int) -> Item:
    if id not in items_db or items_db[id].deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return items_db[id]

async def get_items(
        offset: int = 0,
        limit: int = 10,
        min_price: float = None,
        max_price: float = None,
        show_deleted: bool = False
) -> List[Item]:
    items = list(items_db.values())
    filtered_items = []
    for item in items:
        if not show_deleted and item.deleted:
            continue
        if min_price is not None and item.price < min_price:
            continue
        if max_price is not None and item.price > max_price:
            continue
        filtered_items.append(item)
    return filtered_items[offset : offset + limit]

async def put_item(id: int, req: ItemPutRequest) -> Item:
    if id not in items_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    item = items_db[id]
    if item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED)
    item.name = req.name
    item.price = req.price
    return item

async def patch_item(id: int, req: ItemPatchRequest) -> Item:
    if id not in items_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    item = items_db[id]
    if item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED)
    for key, value in req:
        setattr(item, key, value)
    return item

def delete_item(id: int):
    if id not in items_db:
        return "Товар уже удален"
    item = items_db[id]
    if item.deleted:
        return "Товар уже удален"
    item.deleted = True
    return "Товар удален"