from hw_2.controllers import cart, item
import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Shop API")

app.get(
    path="/ping"
)
def pong():
    return {"message": "pong"}

app.include_router(cart.router)
app.include_router(item.router)

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)