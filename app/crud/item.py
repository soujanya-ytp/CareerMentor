from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate


def create_item(session: Session, payload: ItemCreate) -> Item:
    item = Item(name=payload.name, description=payload.description)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def list_items(session: Session) -> list[Item]:
    result = session.execute(select(Item).order_by(Item.id))
    return list(result.scalars().all())


def get_item(session: Session, item_id: int) -> Item | None:
    result = session.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()
