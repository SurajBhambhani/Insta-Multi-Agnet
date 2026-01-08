
import uuid


def test_mcp_message_roundtrip(client):
    thread_id = uuid.uuid4().hex
    payload = {
        "thread_id": thread_id,
        "sender": "AgentA",
        "recipient": "broadcast",
        "message": {"hello": "world"},
        "confidence": 0.8,
        "citations": ["test"],
    }
    created = client.post("/mcp/messages", json=payload)
    assert created.status_code == 200
    data = created.json()
    assert data["thread_id"] == thread_id

    fetched = client.get(f"/mcp/messages?thread_id={thread_id}")
    assert fetched.status_code == 200
    assert len(fetched.json()) == 1
