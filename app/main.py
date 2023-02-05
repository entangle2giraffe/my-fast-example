from fastapi import Depends, FastAPI

from . import models
from .database import engine
from .dependencies import get_query_token
from .routers import users, items

models.Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)