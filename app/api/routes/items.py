from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.item import create_item, get_item, list_items
from app.db.session import get_db_session
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
async def read_items(
    session: AsyncSession = Depends(get_db_session),
) -> list[ItemRead]:
    return await list_items(session)


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(
    item_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> ItemRead:
    item = await get_item(session, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(
    payload: ItemCreate,
    session: AsyncSession = Depends(get_db_session),
) -> ItemRead:
    try:
        return await create_item(session, payload)
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item with this name already exists",
        ) from exc
