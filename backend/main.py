from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException

from backend.core.database import close_orm, init_orm
from backend.core.exceptions import http_exception_handler
from backend.users.routers import users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Startup")
    await init_orm()
    yield
    print("Shutdown")
    await close_orm()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.add_exception_handler(HTTPException, http_exception_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
