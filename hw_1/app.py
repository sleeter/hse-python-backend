import math
import json
from typing import Any, Awaitable, Callable
from urllib.parse import parse_qs
from http import HTTPStatus

async def app(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    method = scope['method']
    path = scope['path'].strip('/').split('/')
    if method == 'GET':
        if path[0] == 'factorial':
            await factorial_handler(scope, receive, send)
        elif path[0] == 'fibonacci':
            await fibonacci_handler(scope, receive, send)
        elif path[0] == 'mean':
            await mean_handler(scope, receive, send)
        else:
            await send_404(send)
    else:
        await send_404(send)


async def factorial_handler(scope, receive, send):
    query_params = parse_qs(scope['query_string'].decode())
    n = query_params.get("n", "")
    if n == "":
        await send_422(send)
        return
    if is_int(n[0]) == False:
        await send_422(send)
        return
    n = int(n[0])
    if n < 0:
        await send_400(send)
        return
    factorial = math.factorial(n)
    await send_ok(send, {'result': factorial})


async def fibonacci_handler(scope, receive, send):
    path = scope['path'].split('/')
    if len(path) != 3:
        await send_422(send)
        return
    n = path[2]
    if is_int(n) == False:
        await send_422(send)
        return
    n = int(n)
    if n < 0:
        await send_400(send)
        return
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    await send_ok(send, {'result': a})


async def mean_handler(scope, receive, send):
    body = await get_body(receive)
    try:
        data = json.loads(body)
        if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
            await send_422(send)
            return
    except (json.JSONDecodeError):
        await send_422(send)
        return
    if not data:
        await send_400(send)
        return
    await send_ok(send, {'result': sum(data)/len(data)})




async def send_response(
        send: Callable[[dict[str, Any]], Awaitable[None]],
        code: HTTPStatus,
        body: dict[str, Any],
) -> None:
    await send({
        'type': 'http.response.start',
        'status': code,
        'headers': [
            [b'content-type', b'application/json'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(body).encode('utf-8'),
    })

async def send_error(
        send: Callable[[dict[str, Any]], Awaitable[None]],
        code: HTTPStatus,
        message: str
) -> None:
    await send_response(send, code, {'message': message})

async def send_ok(
        send: Callable[[dict[str, Any]], Awaitable[None]],
        body: dict[str, Any],
) -> None:
    await send_response(send, HTTPStatus.OK, body)

async def send_404(send: Callable[[dict[str, Any]], Awaitable[None]], message: str = "Not Found") -> None:
    await send_error(send, HTTPStatus.NOT_FOUND, message)

async def send_400(send: Callable[[dict[str, Any]], Awaitable[None]], message: str = "Bad Request") -> None:
    await send_error(send, HTTPStatus.BAD_REQUEST, message)

async def send_422(send: Callable[[dict[str, Any]], Awaitable[None]], message: str = "Unprocessable Entity") -> None:
    await send_error(send, HTTPStatus.UNPROCESSABLE_ENTITY, message)

async def get_body(receive: Callable[[], Awaitable[dict[str, Any]]]):
    body = b""
    more_body = True
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    return body.decode()

def is_int(n: str) -> bool:
    try:
        int(n)
        return True
    except ValueError:
        return False