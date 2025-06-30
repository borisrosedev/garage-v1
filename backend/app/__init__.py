from typing import Annotated
from fastapi import FastAPI,HTTPException, Query, Depends
from .database.models import User, Item
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables, SessionDep
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/auth/login")
async def auth_login():
    pass


# FILES


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# ITEMS


@app.post("/api/v1/items/create")
async def create_item(item: Item, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.put("/api/v1/items/{item_id}")
async def update_item(item_id: int, item: Item, token: Annotated[str, Depends(oauth2_scheme)]):
    return {"item_id": item_id, **item.dict()}



@app.get("/api/v1/items")
def read_items(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Item]:
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items



@app.get("/api/v1/items/{item_id}")
def read_item(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/api/v1/items/{item_id}")
def delete_item(item_id: int, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item_id)
    session.commit()
    return {"ok": True}


# USERS

@app.get("/api/v1/users/me")
async def read_user_me(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"user_id": "the current user"}


@app.get("/api/v1/users/")
async def read_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"user_id": "the current user"}


@app.post("/api/v1/users/create")
async def auth_login(user: User):
    user_dict = user.dict()
    return user_dict
