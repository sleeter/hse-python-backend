from typing import Dict, List
from hw_2.models.models import Cart, CartItem
from http import HTTPStatus
from fastapi import HTTPException
from .item import items_db

carts_db: Dict[int, Cart] = {}
cart_id_counter = 0

async def create_cart() -> Cart:
    global cart_id_counter
    cart = Cart(id=cart_id_counter)
    carts_db[cart_id_counter] = cart
    cart_id_counter += 1
    return cart

async def get_cart_by_id(id: int) -> Cart:
    if id not in carts_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    cart = carts_db[id]
    price = 0.0
    quantity = 0
    for cart_item in cart.items:
        item = items_db[cart_item.id]
        if item:
            cart_item.available = not item.deleted
            cart_item.name = item.name
            price += item.price * cart_item.quantity
            quantity += cart_item.quantity
        else:
            cart_item.available = False
    cart.price = price
    cart.quantity = quantity
    return cart

async def get_carts(
        offset: int = 0,
        limit: int = 10,
        min_price: float = None,
        max_price: float = None,
        min_quantity: int = None,
        max_quantity: int = None,
) -> List[Cart]:
    filtered_carts = []
    for cart in list(carts_db.values()):
        price = 0.0
        quantity = 0
        for cart_item in cart.items:
            item = items_db[cart_item.id]
            if item and not item.deleted:
                price += item.price * cart_item.quantity
                quantity += cart_item.quantity
        cart.price = price
        cart.quantity = quantity
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        if min_quantity is not None and quantity < min_quantity:
            continue
        if max_quantity is not None and quantity > max_quantity:
            continue
        filtered_carts.append(cart)
    return filtered_carts[offset : offset + limit]

async def add_item_to_cart(cart_id: int, item_id: int) -> str:
    if cart_id not in carts_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    if item_id not in items_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    cart = carts_db[cart_id]
    item = items_db[item_id]

    if cart and item:
        for cart_item in cart.items:
            if cart_item.id == item.id:
                cart_item.quantity += 1
                break
        else:
            cart.items.append(CartItem(id=item.id, name=item.name, quantity=1, available=not item.deleted))
    else:
        return None
    return "Товар добавлен в корзину"
