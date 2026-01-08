from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_db
from ..services.mcp_bus import list_messages, publish_message
from ..services.serializers import mcp_message_out

router = APIRouter(prefix="/mcp")


@router.post("/messages", response_model=schemas.MCPMessageOut)
def post_message(payload: schemas.MCPMessageIn, db: Session = Depends(get_db)):
    message = publish_message(db, payload)
    return mcp_message_out(message)


@router.get("/messages", response_model=list[schemas.MCPMessageOut])
def get_messages(thread_id: str, recipient: str = "", db: Session = Depends(get_db)):
    items = list_messages(db, thread_id=thread_id, recipient=recipient)
    return [mcp_message_out(item) for item in items]
