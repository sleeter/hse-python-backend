from fastapi import APIRouter, Query, Response
from typing import Optional
import hw_2.services.cart as cartService
from http import HTTPStatus


router = APIRouter(prefix="/cart")

@router.post("/", status_code=HTTPStatus.CREATED)
async def post_cart(response: Response):
    cart = await cartService.create_cart()
    response.headers["location"] = f"/cart/{cart.id}"
    return cart


@router.get("/{cart_id}")
async def get_cart(cart_id: int):
    cart = await cartService.get_cart_by_id(cart_id)
    return cart

@router.get("/")
async def get_carts(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        min_price: Optional[float] = Query(None, ge=0.0),
        max_price: Optional[float] = Query(None, ge=0.0),
        min_quantity: Optional[int] = Query(None, ge=0),
        max_quantity: Optional[int] = Query(None, ge=0),
):
    carts = await cartService.get_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)
    return carts

@router.post("/{cart_id}/add/{item_id}")
async def add_item_to_cart(cart_id: int, item_id: int):
    resp = await cartService.add_item_to_cart(cart_id, item_id)
    return resp