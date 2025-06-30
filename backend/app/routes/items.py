from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from typing import Annotated
from ..database import SessionDep
from ..database.models import Item
from ..core.security import oauth2_scheme

router = APIRouter(prefix="/api/v1/items", tags=["items"])  # Correction: "itesm" → "items"


@router.get("/", response_model=list[Item])
def read_items(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Item]:
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items


@router.post("/create", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: Item,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item: Item,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
