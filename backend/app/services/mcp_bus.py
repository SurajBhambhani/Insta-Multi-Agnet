from typing import Optional

from sqlalchemy.orm import Session

from .. import models, schemas
from ..utils.json_utils import dump_json, load_json


def publish_message(db: Session, payload: schemas.MCPMessageIn) -> models.AgentMessage:
    message = models.AgentMessage(
        thread_id=payload.thread_id,
        sender=payload.sender,
        recipient=payload.recipient,
        message=dump_json(payload.message),
        confidence=payload.confidence,
        citations=dump_json(payload.citations),
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_messages(
    db: Session,
    thread_id: str,
    recipient: Optional[str] = None,
) -> list[models.AgentMessage]:
    query = db.query(models.AgentMessage).filter(models.AgentMessage.thread_id == thread_id)
    if recipient:
        query = query.filter(models.AgentMessage.recipient == recipient)
    return query.order_by(models.AgentMessage.created_at.asc()).all()


def serialize_messages(messages: list[models.AgentMessage]) -> list[dict]:
    serialized = []
    for item in messages:
        serialized.append(
            {
                "sender": item.sender,
                "recipient": item.recipient,
                "message": load_json(item.message, {}),
                "confidence": item.confidence,
                "citations": load_json(item.citations, []),
                "created_at": item.created_at,
            }
        )
    return serialized
