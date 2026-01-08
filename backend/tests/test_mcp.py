
def test_mcp_message_roundtrip(client):
    payload = {
        "thread_id": "thread-1",
        "sender": "AgentA",
        "recipient": "broadcast",
        "message": {"hello": "world"},
        "confidence": 0.8,
        "citations": ["test"],
    }
    created = client.post("/mcp/messages", json=payload)
    assert created.status_code == 200
    data = created.json()
    assert data["thread_id"] == "thread-1"

    fetched = client.get("/mcp/messages?thread_id=thread-1")
    assert fetched.status_code == 200
    assert len(fetched.json()) == 1
